# Copyright 2024 Wirepas Ltd licensed under Apache License, Version 2.0
#
# See file LICENSE for full license details.
#
import argparse

import logging
import json
import ssl
from time import sleep, time
from enum import Enum, auto
from threading import Thread, Lock
from typing import Any, List
import os
import sys

import paho.mqtt.client as mqtt
from google.protobuf import json_format

from wirepas_wpe_apt import common_functions as cf
from wirepas_wpe_apt.constants import *
from wirepas_wpe_apt.element import Node

from wirepas_wpe_apt import wpe_proto


# WPE MQTT topics
MQTT_TOPIC_RESPONSE: str = "wpe-response"
MQTT_TOPIC_ALL_RESPONSES: str = MQTT_TOPIC_RESPONSE + "/#"
MQTT_TOPIC_RESPONSE_PURGE: str = MQTT_TOPIC_RESPONSE + "/purge"
MQTT_TOPIC_RESPONSE_CONFIGURE: str = MQTT_TOPIC_RESPONSE + "/configure"
MQTT_TOPIC_RESPONSE_FETCH: str = MQTT_TOPIC_RESPONSE + "/fetch"
MQTT_TOPIC_RESPONSE_LOCATE: str = MQTT_TOPIC_RESPONSE + "/locate"

MQTT_TOPIC_REQUEST: str = "wpe-request"
MQTT_TOPIC_REQUEST_PURGE: str = MQTT_TOPIC_REQUEST + "/purge"
MQTT_TOPIC_REQUEST_CONFIGURE: str = MQTT_TOPIC_REQUEST + "/configure"
MQTT_TOPIC_REQUEST_FETCH: str = MQTT_TOPIC_REQUEST + "/fetch"
MQTT_TOPIC_REQUEST_LOCATE: str = MQTT_TOPIC_REQUEST + "/locate"


SLEEP_WAITING_IN_S = 0.1


class PlaybackStateEnum(Enum):
    """ Playback state enumerate. """
    NOT_STARTED = auto()
    CONNECTED_TO_MQTT = auto()
    PURGE = auto()
    CONFIGURE = auto()
    FETCH = auto()
    LOCATE = auto()
    FINISHED = auto()


class ConnectionResultEnum(Enum):
    """ Connection result values for MQTT on connect callback. """
    SUCCESS = 0
    INCORRECT_PROTOCOL_VERSION = 1
    INVALID_CLIENT_IDENTIFIER = 2
    SERVER_UNAVAILABLE = 3
    BAD_CREDENTIALS = 4
    NOT_AUTHORISED = 5


class Playback(Thread):
    def __init__(self, configuration_file_name, folder_path="wpeapt_data",
                 wpe_max_inflight_messages=50, timeout_s=60):
        """ The playback subscribes to topics on the WPE MQTT and configure WPE with
        anchors/areas for a network thanks to the data retrieved by the
        data collector (i.e. configuration & measurement data file),
        and then playbacks the measurements, and stores computed locations
        in a new file.

        note: playback won't compute locations of nodes if they are referred to anchors
            nodes in the configuration data file.

        Args:
            configuration_file_name (str): Name of the configuration file to
                access WPE MQTT (refer to the module documentation).
            folder_path: Default to "wpeapt_data". Path of the folder to store the collected data.
            timeout_s (int): Default to 60.
                Time interval in seconds allowed for not receiving any response by the backend.
            wpe_max_inflight_messages (int): Default to 50.
                Max number of simultaneous messages that are sent to the backend.
        """
        super(Playback, self).__init__()

        self.publish_authorisation_lock = Lock()
        self.timeout_s = timeout_s
        self.waiting_time_start = time()  # Used for timeout, it is reset each time a message is received.
        self.wpe_max_inflight_messages = wpe_max_inflight_messages
        self.inflight_messages_nb = 0
        self.playback_state = PlaybackStateEnum.NOT_STARTED

        # Setup the mqtt client.
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_message = self.on_message_cb_generator()
        self.mqtt_client.on_connect = self.on_connect_cb_generator()
        self.mqtt_client.on_disconnect = self.on_disconnect_cb_generator()

        # Input and output files
        self.folder_path = folder_path
        self.configuration_file = os.path.join(self.folder_path, "data", "network_configuration.json")
        self.computed_locations_file = os.path.join(self.folder_path, "data", "computed_locations.json")

        # Parse the credentials configuration.
        try:
            configuration_data = cf.get_data_json(configuration_file_name)
            self.mqtt_client.username_pw_set(configuration_data["wpe_mqtt_username"],
                                             configuration_data["wpe_mqtt_password"])
            self.mqtt_hostname = configuration_data["wpe_mqtt_hostname"]
            self.mqtt_port = configuration_data.get("wpe_mqtt_port", 8883)
            self.mqtt_client.tls_set(
                ca_certs=configuration_data.get("wpe_mqtt_ca_certs"),
                certfile=configuration_data.get("wpe_mqtt_certfile"),
                keyfile=configuration_data.get("wpe_mqtt_keyfile"),
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLSv1_2,
                ciphers=configuration_data.get("wpe_mqtt_ciphers"),
            )
        except KeyError as error:
            raise KeyError("The configuration file should contain all the values "
                           "needed for the script to work properly. "
                           "Check the README.md for more information!") from error

        # Data used for the playback
        self.network_data = cf.parse_elements_file(self.configuration_file)
        self.network_id = int(self.network_data[NETWORK_FIELD])
        self.received_measurements = []
        self.received_measurements_lock = Lock()

        measurements = self.network_data.get(MEASUREMENTS_FIELD)

        # Check relevant data are complete.
        assert self.network_data.get(NODES_FIELD), \
            "No anchors have been found! Verify that the Data Collector could collect anchor data!"
        assert measurements, \
            "No measurements have been found! Verify that the Data Collector could collect measurements!"

    def add_handlers(self):
        """ Function used to add callbacks when the client receives messages. """
        logging.info("adding message callbacks on purge, configure, fetch, locate")
        self.mqtt_client.message_callback_add(MQTT_TOPIC_RESPONSE_PURGE, self.handle_response_purge)
        self.mqtt_client.message_callback_add(MQTT_TOPIC_RESPONSE_CONFIGURE, self.handle_response_configure)
        self.mqtt_client.message_callback_add(MQTT_TOPIC_RESPONSE_FETCH, self.handle_response_fetch)
        self.mqtt_client.message_callback_add(MQTT_TOPIC_RESPONSE_LOCATE + f"/{self.network_id}",
                                              self.handle_response_locate)

    def _on_connect_callback(self, mqtt_client, userdata, flags, rc):
        """ Callback that is called when connection to MQTT has succeeded.

        Args:
           mqtt_client (object): The MQTT client instance for this callback.
           userdata (object): The private user data.
           flags (list): A list of flags.
           rc (int): The connection result.
        """
        logging.info("Trying to connect")

        # Check the connection result.
        if rc == ConnectionResultEnum.SUCCESS.value:
            logging.info("Connected to MQTT")
            self.playback_state = PlaybackStateEnum.CONNECTED_TO_MQTT
        elif rc == ConnectionResultEnum.INCORRECT_PROTOCOL_VERSION.value:
            logging.error("WPE MQTT Error: Incorrect protocol version")
            raise ValueError
        elif rc == ConnectionResultEnum.INVALID_CLIENT_IDENTIFIER.value:
            logging.error("WPE MQTT Error: Invalid client identifier")
            raise ValueError
        elif rc == ConnectionResultEnum.SERVER_UNAVAILABLE.value:
            logging.error("WPE MQTT Error: Server unavailable")
            raise ValueError
        elif rc == ConnectionResultEnum.BAD_CREDENTIALS.value:
            logging.error("WPE MQTT Error: Bad username or password")
            raise ValueError
        elif rc == ConnectionResultEnum.NOT_AUTHORISED.value:
            logging.error("WPE MQTT Error: Not authorised")
            raise ValueError
        else:
            logging.error(f"WPE MQTT Error: Unknown error: {rc}")
            raise ValueError

    def _on_message_callback(self, client, userdata, msg):
        """ Gets data from the input topic.

        Args:
            client: MQTT client object.
            userdata: the private user data
            msg: Incoming message
        """
        logging.info(f"Incoming <- {msg.topic}[qos:{msg.qos}]:{msg.payload}")

    def on_connect_cb_generator(thread) -> Any:
        """ Callback generator for on_connect MQTT callbacks.

        Args:
            thread: That has the callback function.

        Return: A callback function.
        """

        def on_connect(client, userdata, flags: List[bool], rc: int):
            """ A function to call the thread callback method.

            Args:
               client: The client instance for this callback.
               flags: List of flags.
               userdata: The private user data.
               rc: The connection result.
            """
            thread._on_connect_callback(client, userdata, flags, rc)

        return on_connect

    def on_message_cb_generator(thread) -> Any:
        """ Callback generator for on_message MQTT callbacks.

        Args:
            thread: That has the callback function.

        Return: A callback function.
        """

        def on_message(client, userdata, msg):
            """ A function to call the thread callback method.

            Args:
               client: The client instance for this callback.
               userdata: The private user data.
               msg: Message.
            """
            thread._on_message_callback(client, userdata, msg)

        return on_message

    def on_disconnect_cb_generator(thread) -> Any:
        """ Callback generator for on_disconnect MQTT callbacks.

        Args:
            thread: That has the callback function.

        Return: A callback function.
        """

        def on_disconnect(client, userdata, rc: int):
            """ A function to call the thread callback method.

            Args:
               client: The client instance for this callback.
               userdata: The private user data.
               rc: The connection result.
            """
            logging.info("WNT disconnected! Retrying to connect")

        return on_disconnect

    def get_authorisation_to_publish(self):
        """ Get the autorisation to publish message to the MQTT broker. """
        with self.publish_authorisation_lock:
            while not self.mqtt_client.is_connected() or \
                    self.inflight_messages_nb >= self.wpe_max_inflight_messages:
                sleep(SLEEP_WAITING_IN_S)

            self.inflight_messages_nb += 1

    def publish_message(self, payload, topic):
        """ Publish a message on the MQTT broker. """
        self.get_authorisation_to_publish()

        logging.info("Publish a message on %s", topic)
        logging.debug("Publish the payload %s", payload)
        pubinfo = self.mqtt_client.publish(
            payload=payload,
            topic=topic
        )

        if pubinfo.rc != mqtt.MQTT_ERR_SUCCESS:
            logging.info("publish: {0} ({1})".format(
                mqtt.error_string(pubinfo.rc), pubinfo.rc)
            )
        try:
            pubinfo.wait_for_publish()
        except ValueError:
            logging.error("A message could not be pushed to the MQTT broker.")

    def handle_response_dec(fn):
        """ Decorator to handle responses from the mqtt broker. """
        def wrapper(self, *args, **kwargs):
            self.inflight_messages_nb -= 1
            return fn(self, *args, **kwargs)

        return wrapper

    @handle_response_dec
    def handle_response_purge(self, client, userdata, message):
        """
        Function called when a purge response is received.
        Also verify if the purge request did not failed.

        Example of answers showing the well working of the WPE for the network xxxxxxx :
            {'code': 'ERROR', 'message': 'Unknown network xxxxxxx', 'sender': ''}
            {'code': 'SUCCESS', 'message': 'Deleted all the configuration for network xxxxxxx', 'sender': ''}
        """
        logging.info("Handle purge response")
        response = wpe_proto.Status()
        response.ParseFromString(message.payload)
        resp_dict = json_format.MessageToDict(response, preserving_proto_field_name=True)

        logging.debug("Handle purge response:\n{}".format(resp_dict))
        if 'Unknown network' in resp_dict[MESSAGE_FIELD] and str(self.network_id) in resp_dict[MESSAGE_FIELD]:
            logging.debug(f"Nothing to purge in the network {self.network_id}")
            self.playback_state = PlaybackStateEnum.CONFIGURE
        elif (resp_dict[MESSAGE_FIELD] == f'Deleted all the configuration for network {self.network_id}'
              and resp_dict["code"] != "SUCCESS"):
            logging.error("Purge of network %d failed.", self.network_id)
            raise ValueError
        elif resp_dict["code"] == "SUCCESS" and str(self.network_id) in resp_dict[MESSAGE_FIELD]:
            self.playback_state = PlaybackStateEnum.CONFIGURE

    @handle_response_dec
    def handle_response_configure(self, client, userdata, message):
        """
        Function called when a configuration response is received.
        Also verify if the configuration request did not failed.

        Example of answers showing the well working of the WPE for the network xxxxxxx :
            {'code': 'SUCCESS', 'message': "{'network': 'xxxxxxx', 'is_new_network': True, 'nodes_nb': 2}", 'sender': ''}
        """
        logging.info("Handle configure response")
        response = wpe_proto.Status()
        response.ParseFromString(message.payload)
        resp_dict = json_format.MessageToDict(response, preserving_proto_field_name=True)

        logging.debug("Handle configure response:\n{}".format(resp_dict))
        if resp_dict["code"] == "SUCCESS":
            self.playback_state = PlaybackStateEnum.FETCH
        elif f"'{self.network_id}'" in resp_dict[MESSAGE_FIELD] and resp_dict["code"] != "SUCCESS":
            logging.error(f"Configure of the network {self.network_id} failed.")
            raise ValueError

    @handle_response_dec
    def handle_response_fetch(self, client, userdata, message):
        """
        Function called when a fetch response is received.
        If the WPE answered correctly,
        message will show a wpe_proto.ConfigurationData()
        with the shape of a json format.

        Also verify if the fetch message correspond to the network sent.
        """
        logging.info("Handle fetch response")
        response = wpe_proto.ConfigurationData()
        response.ParseFromString(message.payload)
        resp_network = json_format.MessageToDict(response, preserving_proto_field_name=True)

        # verification that we didn't lose any anchors between configuration and fetch queries
        logging.debug("Handle fetch response:\n{}".format(resp_network))
        if resp_network[NETWORK_FIELD] == self.network_data[NETWORK_FIELD]:
            self.waiting_time_start = time()  # Timeout must be reset as we received a message.
            if NODES_FIELD in self.network_data:
                assert len(self.network_data[NODES_FIELD]) == len(resp_network[NODES_FIELD]),\
                        f"Configuration of the network {self.network_id}" \
                        "is not the same as the one sent."

                for node in resp_network[NODES_FIELD]:
                    if not cf.search_node(resp_network, node[ADDRESS_FIELD]):
                        logging.error((f"Configuration of the network {self.network_id} is not the same as the one sent."))
                        raise ValueError

            self.playback_state = PlaybackStateEnum.LOCATE

    @handle_response_dec
    def handle_response_locate(self, client, userdata, message):
        """
        Function called when a locate response is received.
        If the WPE answered correctly, message will show a wpe_proto.Node()
        with the shape of a json format.

        Also verify if the locate message correspond to the network sent.
        """
        response = wpe_proto.Node()
        response.ParseFromString(message.payload)
        location_dict = Node.from_wpe_proto(response).to_dict()
        if location_dict["network_id"] != self.network_id:
            return

        with self.received_measurements_lock:
            self.waiting_time_start = time()  # Timeout must be reset as we received a message.
            self.received_measurements.append(location_dict)
            logging.info("Handle locate response [%d/%d]",
                         len(self.received_measurements),
                         len(self.network_data[MEASUREMENTS_FIELD]))
            logging.debug("Handle locate response:\n{}".format(location_dict))

        if len(self.received_measurements) == len(self.network_data[MEASUREMENTS_FIELD]):
            self.playback_state = PlaybackStateEnum.FINISHED

    def wait_for_state(self, state: PlaybackStateEnum):
        """ Wait for the module to get the required state before continuing.
        Return False if the timeout has been reached, True otherwise.
        """
        self.waiting_time_start = time()
        while self.playback_state != state \
                and (not self.timeout_s or time() < self.timeout_s + self.waiting_time_start):
            sleep(SLEEP_WAITING_IN_S)

        return not self.timeout_s or time() < self.timeout_s + self.waiting_time_start

    def _query(self):
        """
        Function in charge of all queries : purge query, configure query,
        fetch query and locate queries.
        More precisely, initiate the message to query and
        send them with the MQTT client.

        Warning: Note that it will clean the current network with the same id
                 of the same service.
        """
        logging.info("Querying WPE mqtt broker to playback data from the network %s", self.network_id)
        if not self.wait_for_state(PlaybackStateEnum.CONNECTED_TO_MQTT):
            logging.error("Playback FSM state is not connected to the MQTT "
                          "but _query method was called! Actual step: %s",
                          self.playback_state)
            raise ValueError

        # Purge the network
        self.playback_state = PlaybackStateEnum.PURGE
        purge_data = wpe_proto.Query()
        purge_data.network = self.network_id
        self.publish_message(purge_data.SerializeToString(), MQTT_TOPIC_REQUEST_PURGE)

        # Configuration of the network on the WPE
        if not self.wait_for_state(PlaybackStateEnum.CONFIGURE):
            logging.error("Playback FSM state could not reach configure network step! "
                          "Actual step: %s",
                          self.playback_state)
            raise ValueError

        configuration_data = cf.network_to_configurationdata(self.network_data)
        self.publish_message(configuration_data.SerializeToString(), MQTT_TOPIC_REQUEST_CONFIGURE)

        # Verification that the configuration of the network went well
        if not self.wait_for_state(PlaybackStateEnum.FETCH):
         logging.error("Playback FSM state could not reach fetch network step! "
                       "Actual step: %s", self.playback_state)
         raise ValueError

        fetch_data = wpe_proto.Query()
        fetch_data.network = self.network_id
        self.publish_message(fetch_data.SerializeToString(), MQTT_TOPIC_REQUEST_FETCH)

        # Location queries
        if not self.wait_for_state(PlaybackStateEnum.LOCATE):
         logging.error("Playback FSM state could not reach locate nodes step! "
                       "Actual step: %s", self.playback_state)
         raise ValueError

        for measurement in self.network_data[MEASUREMENTS_FIELD]:
            measurement = measurement.to_wpe_proto()
            self.publish_message(measurement.SerializeToString(), MQTT_TOPIC_REQUEST_LOCATE)

        if not self.wait_for_state(PlaybackStateEnum.FINISHED):
         logging.error("Playback FSM state did not receive all location responses! "
                       "Actual step: %s", self.playback_state)
         raise ValueError

    def save_results(self):
        """ Store locations received by the MQTT client. """
        content = {
            NETWORK_FIELD: str(self.network_id),
            NODES_FIELD: self.received_measurements
        }

        logging.info("Save newly computed locations to %s", self.computed_locations_file)
        with open(self.computed_locations_file, 'w', newline='') as data_file:
            json.dump(content, data_file, indent=4)

    def run_playback(self):
        """
        Make MQTT client connect to the server, subscribe to the MQTT all responses topic,
        configure callbacks and clean network
        with the id network_id to configure a new one with
        the data of file_name. Then, playback measurements and store
        the computed positions in the file put in argument.

        Warning: Note that it will clean the current network with the same id
                 of the same service.
        """
        self.mqtt_client.connect(self.mqtt_hostname, self.mqtt_port)
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe(MQTT_TOPIC_ALL_RESPONSES)
        self.add_handlers()
        self._query()
        self.save_results()
        logging.info("Exiting")


def str2int(value):
    if value:
        return int(value)
    else:
        raise ValueError("Unrecognised int value")


def main():
    """
    Example of use:
    python3 ./playback.py --configuration="example_configuration.json" \
            --folder_path="wpeapt_data"
    """
    # Argument parser
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('--configuration', type=str, required=True,
                        help='Configuration file name')
    parser.add_argument('--folder_path', type=str, default="wpeapt_data",
                        help='Default to "wpeapt_data". '
                        'Path of the folder to store the collected data.')
    parser.add_argument("--log_level", default="info", type=str,
                        choices=["debug", "info", "warning", "error", "critical"],
                        help="Log level to be displayed.")
    parser.add_argument("--wpe_max_inflight_messages", type=str2int, default=50,
                        help="Default to 50. Max number of simultaneous messages that are sent to the backend.")
    parser.add_argument("--timeout_s", type=str2int, default=60,
                        help="Default to 60. Time interval in seconds allowed for not receiving response by the backend.")

    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s | [%(levelname)s] %(filename)s:%(lineno)d:%(funcName)s:%(message)s',
        level=args.log_level.upper(),
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("playback.log", mode="w")
        ]
    )

    # Run the playback tool with provided parameters
    mqtt_handler = Playback(
        configuration_file_name=args.configuration,
        folder_path=args.folder_path,
        wpe_max_inflight_messages=args.wpe_max_inflight_messages,
        timeout_s=args.timeout_s)

    mqtt_handler.run_playback()


if __name__ == "__main__":
    main()
