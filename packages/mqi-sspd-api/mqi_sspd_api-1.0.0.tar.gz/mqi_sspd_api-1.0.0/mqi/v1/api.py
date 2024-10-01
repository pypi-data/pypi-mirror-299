# Copyright 2024 The MQI Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import websocket
import json
import time
from typing import List, Any
import hashlib
"""MQI is the main entry point of the api used to do most high level tasks"""
class MQI:
    """
        Initializes the MQI object.

        :param hostname: Hostname for connection.
        :param port: Port for connection.
        :param username: Username for authentication.
        :param password: Password for authentication.

        :returns: None
    """
    def __init__(self, hostname : str, port : str, username : str, password : str):
        self.hostname = hostname 
        self.port = port
        self.ws = None 
        self.uniq_number = 0
        self.connect()
        password_bytes = password.encode('utf-8')
        self.auth_token = self.__gen_auth_token(username, hashlib.sha256(password_bytes).hexdigest())

    """
    connect function will create a connection to the cosen Raspberry Pi websocket. 
    If there is no avaialable a "NotFound" error is returned.

    :returns: None
    """
    def connect(self):
        self.ws = websocket.WebSocket()
        self.ws.connect(self.hostname + ":" + self.port)
        message = self.ws.recv()
    """
        Receives a response from the websocket.

        :returns: Decoded JSON response.
    """
    def __get_response(self):
        message = self.ws.recv()
        response = json.loads(message)
        return response

    """
        Converts a list to a string.

        :param lst: List to convert.

        :returns: String representation of the list.
    """
    def __list_to_string(self, lst : List[Any]) -> str:
        result = [str(ch_id) for ch_id in lst]

        return result

    """
        Generates an authentication token.

        :param username: Username.
        :param password: Password.

        :returns: Authentication token.
    """
    def __gen_auth_token(self, username: str, password: str):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "LOGIN",
                "uid": uid,
                "timestamp": str(time.time()),
                "body" : {
                    "username" : username,
                    "password" : password
                }
        }
        self.uniq_number = (self.uniq_number + 1) % 1000000
        self.ws.send(json.dumps(data))
        response = self.__get_response()
        print(f"uid: {response['uid']}, status: {response['status']}")

        return response["body"]["token"]

    """
        Requests the status of a specific Arduino.

        :param arduino_id: The ID of the Arduino.

        :returns: None
    """
    def get_status(self, arduino_id : int):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "REQ_STATUS",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "arduino_id" : arduino_id,
                    "token" : self.auth_token
                }
        }

        self.ws.send(json.dumps(data))
        print(self.ws.recv())

        return None

    """
        Sets the current for specific channels on an Arduino.

        :param arduino_id: The ID of the Arduino.
        :param channel_ids: List of channel IDs.
        :param value: Current value to set.

        :returns: Status of the request.
    """
    def set_current(self, arduino_id : int, chanel_ids : List[int], value : int):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "SET_CURRENT",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "arduino_id" : arduino_id,
                    "channel_ids" : self.__list_to_string(chanel_ids),
                    "value" : value,
                    "token" : self.auth_token
                }
        }
        self.uniq_number = (self.uniq_number + 1) % 1000000
        self.ws.send(json.dumps(data))
        response = self.__get_response()
        print(f"uid: {response['uid']}, status: {response['status']}")

        return response["status"]

    """
        Sets the voltage for specific channels on an Arduino.

        :param arduino_id: The ID of the Arduino.
        :param channel_ids: List of channel IDs.
        :param value: Voltage value to set.

        :returns: Status of the request.
    """
    def set_voltage(self, arduino_id : int, chanel_ids : List[int], value : int):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "SET_VOLTAGE",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "arduino_id" : arduino_id,
                    "channel_ids" : self.__list_to_string(chanel_ids),
                    "value" : value,
                    "token" : self.auth_token
                }
        }
        self.uniq_number = (self.uniq_number + 1) % 1000000
        self.ws.send(json.dumps(data))
        response = self.__get_response()
        print(f"uid: {response['uid']}, status: {response['status']}")

        return response["status"]

    """
        Gets the number of channels for a specific Arduino.

        :param arduino_id: The ID of the Arduino.

        :returns: Number of channels.
    """
    def get_number_of_channels(self, arduino_id : int):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "GET_NUMBER_OF_CHANNELS",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "arduino_id" : arduino_id,
                    "token" : self.auth_token
                }
        }

        self.ws.send(json.dumps(data))
        response = self.__get_response()
        print(f"uid: {response['uid']}, status: {response['status']}")

        return response['body']

    """
        Sets specific channels on an Arduino as active.

        :param arduino_id: The ID of the Arduino.
        :param channel_ids: List of channel IDs.

        :returns: Status of the request.
    """
    def set_channels_active(self, arduino_id : int, chanel_ids : List[int]):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "SET_CHANNELS_ACTIVE",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "arduino_id" : arduino_id,
                    "channel_ids" : self.__list_to_string(chanel_ids),
                    "token" : self.auth_token
                }
        }
        self.uniq_number = (self.uniq_number + 1) % 1000000
        self.ws.send(json.dumps(data))
        response = self.__get_response()
        print(f"uid: {response['uid']}, status: {response['status']}")
        return response["status"]

    """
        Gets the active channels for a specific Arduino.

        :param arduino_id: The ID of the Arduino.

        :returns: List of active channel IDs.
    """
    def get_channels_active(self, arduino_id : int):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "GET_CHANNELS_ACTIVE",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "arduino_id" : arduino_id,
                    "token" : self.auth_token
                }
        }

        self.ws.send(json.dumps(data))
        response = self.__get_response()
        print(f"uid: {response['uid']}, status: {response['status']}")

        return response['body']

    """
        Gets the ADC voltage for specific channels on an Arduino.

        :param arduino_id: The ID of the Arduino.
        :param channel_ids: List of channel IDs.

        :returns: Dictionary with channel voltage information.
    """
    def get_ADC_voltage(self, arduino_id : int, chanel_ids : List[int]):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "GET_VOLTAGE",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "arduino_id" : arduino_id,
                    "channel_ids" : self.__list_to_string(chanel_ids),
                    "token" : self.auth_token
                }
        }
        self.uniq_number = (self.uniq_number + 1) % 1000000
        self.ws.send(json.dumps(data))
        response = self.__get_response()
        print(f"uid: {response['uid']}, status: {response['status']}")

        return response['body']

    """
        Gets the ADC current for specific channels on an Arduino.

        :param arduino_id: The ID of the Arduino.
        :param channel_ids: List of channel IDs.

        :returns: Dictionary with channel current information.
    """
    def get_ADC_current(self, arduino_id : int, chanel_ids : List[int]):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "GET_CURRENT",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "arduino_id" : arduino_id,
                    "channel_ids" : self.__list_to_string(chanel_ids),
                    "token" : self.auth_token
                }
        }
        self.uniq_number = (self.uniq_number + 1) % 1000000
        self.ws.send(json.dumps(data))
        response = self.__get_response()
        print(f"uid: {response['uid']}, status: {response['status']}")

        return response['body']

    """
        Gets the DAC voltage for specific channels on an Arduino.

        :param arduino_id: The ID of the Arduino.
        :param channel_ids: List of channel IDs.

        :returns: Dictionary with channel DAC voltage information.
    """
    def get_DAC_voltage(self, arduino_id : int, chanel_ids : List[int]):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "GET_DAC_VOLTAGE",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "arduino_id" : arduino_id,
                    "channel_ids" : self.__list_to_string(chanel_ids),
                    "token" : self.auth_token
                }
        }
        self.uniq_number = (self.uniq_number + 1) % 1000000
        self.ws.send(json.dumps(data))
        response = self.__get_response()
        print(f"uid: {response['uid']}, status: {response['status']}")

        return response['body']

    """
        Gets the DAC current for an Arduino.

        :param arduino_id: The ID of the Arduino.

        :returns: Dictionary with DAC current information.
    """
    def get_DAC_current(self, arduino_id : int):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "GET_DAC_CURRENT",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "arduino_id" : arduino_id,
                    "token" : self.auth_token
                }
        }

        self.ws.send(json.dumps(data))
        response = self.__get_response()
        print(f"uid: {response['uid']}, status: {response['status']}")

        return response['body']

    """
        Gets the maximum voltage and current for an Arduino.

        :param arduino_id: The ID of the Arduino.

        :returns: Dictionary with maximum voltage and current.
    """
    def get_max_volt_current(self, arduino_id : int):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "GET_MAX_VOLT_CURRENT",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "arduino_id" : arduino_id,
                    "token" : self.auth_token
                }
        }

        self.ws.send(json.dumps(data))
        response = self.__get_response()
        print(f"uid: {response['uid']}, status: {response['status']}")

        return response['body']

    """
        Restarts a specific Arduino.

        :param arduino_id: The ID of the Arduino.

        :returns: Status of the request.
    """
    def restart_arduino(self, arduino_id : int):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "RESTART_ARDUINO",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "arduino_id" : arduino_id,
                    "token" : self.auth_token
                }
        }

        self.ws.send(json.dumps(data))
        response = self.__get_response()
        print(f"uid: {response['uid']}, status: {response['status']}")

        return response["status"]

    """
        Gets the unique ID of a specific Arduino.

        :param arduino_id: The ID of the Arduino.

        :returns: The unique ID of the Arduino.
    """
    def get_id(self, arduino_id : int):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "GET_ID",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "arduino_id" : arduino_id,
                    "token" : self.auth_token
                }
        }

        self.ws.send(json.dumps(data))
        response = self.__get_response()
        print(f"uid: {response['uid']}, status: {response['status']}")

        return response['body']

    """
        Gets the number of Arduinos connected.

        :returns: Number of connected Arduinos.
    """
    def get_numb_of_arduinos(self):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "NUMB_OF_ARDUINOS",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "token" : self.auth_token
                }
        }

        self.ws.send(json.dumps(data))
        response = self.__get_response()
        print(f"uid: {response['uid']}, status: {response['status']}")

        return response['body']

    """
        Restarts the Raspberry Pi.

        :returns: Status of the request.
    """
    def restart_rpi(self):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "RESTART_RPI",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "token" : self.auth_token
                }
        }

        self.ws.send(json.dumps(data))
        response = self.__get_response()
        print(f"uid: {response['uid']}, status: {response['status']}")

        return response["status"]

    """
        TODO: Gets the configuration of a specific Arduino.

        :param arduino_id: The ID of the Arduino.

        :returns: config
    """
    def get_config(self, arduino_id : int):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "GET_CONFIG",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "arduino_id" : arduino_id,
                    "token" : self.auth_token
                }
        }

        self.ws.send(json.dumps(data))
        print(self.ws.recv())

        return None

    """
        Sets the configuration of a specific Arduino.

        :param arduino_id: The ID of the Arduino.

        :returns: request status
    """
    def set_config(self, arduino_id : int):
        uid = f"{time.time()}{self.uniq_number}"
        data = {
                "__MESSAGE__": "message",
                "command": "SET_CONFIG",
                "uid": uid,
                "timestamp": time.time(),
                "body" : {
                    "token" : self.auth_token
                }
        }

        self.ws.send(json.dumps(data))
        print(self.ws.recv())

        return None