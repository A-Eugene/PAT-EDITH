"""
    BLEJSONInstruction.py by A Eugene

    Since Bluetooth Low Energy by default limits each message to 20 bytes,
    sending a large instruction data could have been a challenge. This library
    decodes array of string data into JSON by appending the message into a string
    variable and checks after each append whether the messages has formed
    a JSON or not. 

    If a JSON format is formed, then this class would call all the callbacks in
    self.on_instruction_callbacks which is an array full of callbacks listening
    this event. self.messgae will be cleared.

    If JSON is not formed, then keep appending the message.

    This library can also be used to send JSON instruction to the other peer,
    by using the same mechanism. Stringifying the JSON, split it into array of 
    20 character long strings, then send it all one by one.

    This library depends on ESP32BLE.py
"""

import json
from Libraries.ESP32BLE import ESP32_BLE

class BLEJSONInstruction:
    def __init__(self, bluetooth: ESP32_BLE):
        self.message = ""
        self.bluetooth = bluetooth
        self.on_instruction_callbacks = []

    def on_instruction(self, callback):
        self.on_instruction_callbacks.append(callback)

    def feedChunk(self, chunk: str):
        self.message += chunk
        # print('====')
        # print('Fed message:', chunk)
        # print('self.message:', self.message)
        # print('====')

        # Instruction needs to start with { so it ends up with
        # a dictionary, not array or any other data type
        if not self.message.strip().startswith('{'):
            self.message = ''
            return

        # JSON data that has more "}" than "{" is definitely malformed
        # *ASSUMING that no string values contain "{" or "}"
        if self.message.count('{') < self.message.count('}'):
            self.message = ''
            return 

        try:
            data = json.loads(self.message)

            # Workaround for Micropython's unusual json behaviour
            # See README.md:43

            # If the dictionary is formed but the JSON isn't completed, keep appending new messages
            # Case example: json.loads('{"a": true') returns {"a": True}, leaving the "}" in the next message
            if self.message.count('{') != self.message.count('}'):
                return

            # If JSON is completed (closed) but data equals to {}, consider it as bad instruction
            # and clear the message, ignoring it.
            # Case example: json.loads('{"a": }') returns {} 
            if data == {}:
                self.message = '' 
                return

            for callback in self.on_instruction_callbacks:
                callback(data)

            self.message = "" 
        except Exception as e:
            # Same amount of "{" and "}" means the JSON is completed (closed) or it's not JSON at all
            # If the JSON is completed yet the error persists, it means malformed JSON
            # so self.message needs to be cleared so we can receive new instructions
            if self.message.count('{') == self.message.count('}'):
                # print('Clearing self.message, { and } count:', str(self.message.count('{')), str(self.message.count('}')))
                self.message = "" #

            # print('JSON error:', e)

    # Send a JSON instruction as well
    def sendInstruction(self, message: dict, chunkSize: int = 20):
        stringMsg = json.dumps(message)

        for i in range(0, len(stringMsg), chunkSize):
            self.bluetooth.send(stringMsg[i:i+chunkSize])
