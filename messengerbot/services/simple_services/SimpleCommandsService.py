# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via the online chat services.

    messengerbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    messengerbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with messengerbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
import os
import re
from datetime import timedelta

from messengerbot.servicehandlers.Service import Service
from messengerbot.connection.generic.Message import Message


class SimpleCommandsService(Service):
    """
    The SimpleCommandsService Class that extends the generic Service class.
    The service offers several trivial commands to the user
    """

    identifier = "simple_commands"
    """
    The identifier for this service
    """

    help_description = {"en": "Simple Commands: Collection of Commands that do simple things\n"
                              "/uptime\tDisplays the uptime of the server running the bot",
                        "de": "Simple Befehle: Sammlung von Befehlen die simple Sachen machen\n"
                              "/upzeit\tZeigt die 'uptime' des Servers auf dem der Bot läuft"}
    """
    Help description for this service.
    """

    commands = {"/uptime": "en",
                "/upzeit": "de"}
    """
    List of commands together with the language they are in and the method they call (initialized in initialize())
    """

    uptime_no_uptime_file = {"en": "Uptime command unavailable on this platform",
                             "de": "Upzeit Befehl auf dieser Platform nicht unterstützt"}

    def initialize(self) -> None:
        """
        Initializes the commands dictionary

        :return: None
        """
        self.commands = {"/uptime": ("en", self.get_uptime),
                         "/upzeit": ("de", self.get_uptime)}

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        language = self.commands[message.message_body.lower()][0]
        command = self.commands[message.message_body.lower()][1]

        reply = command(language)
        reply_message = self.generate_reply_message(message, "Simple Command", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^" + Service.regex_string_from_dictionary_keys([SimpleCommandsService.commands]) + "$"
        return re.search(re.compile(regex), message.message_body.lower())

    @staticmethod
    def get_uptime(language: str) -> str:
        """
        Calculates the host PC's uptime and returns it as a string

        :param language: the language in which the command was sent
        :return: the uptime of the computer running the bot
        """
        if not os.path.isfile('/proc/uptime'):
            return SimpleCommandsService.uptime_no_uptime_file[language]

        with open('/proc/uptime', 'r') as uptime_file:
            uptime_seconds = float(uptime_file.readline().split()[0])
            uptime_string = str(timedelta(seconds=uptime_seconds))

        return "Uptime: " + uptime_string