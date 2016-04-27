# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via online chat services.

    messengerbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    messengerbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports

from messengerbot.connection.generic.Connection import Connection
from messengerbot.connection.generic.Message import Message


class Service(object):
    """
    A structure-defining interface for a Service
    """

    has_background_process = False
    """
    Attribute that tells outer classes if this particular service has a background process
    """

    connection = None
    """
    The connection to use to send messages
    """

    help_description = {"en": "A Generic Service Interface",
                        "de": "Eine Generische Dienstleistungsschnittstelle"}
    """
    A dictionary containing help messages in various languages on the use of the service
    """

    identifier = "Service"
    """
    A unique identifier assigned to the plugin.
    """

    def __init__(self, connection: Connection) -> None:
        """
        Basic Constructor for a Service. It stores the connection as a class variable.

        :param connection: The connection to be used by the service
        :return: None
        """
        self.connection = connection

    def send_text_message(self, message: Message) -> None:
        """
        Sends a text message using the active connection and also logs it using the logging mechanism

        :param message: the message to be sent
        :return: None
        """
        # TODO Logging
        self.connection.send_text_message(message)

    def send_image_message(self, receiver: str, message_image: str, caption: str = "") -> None:
        """
        Sends an image to the receiver, with an optional caption/title
        :param receiver: The receiver of the message
        :param message_image: The image to be sent
        :param caption: The caption/title to be displayed along with the image, defaults to an empty string
        :return: None
        """
        # TODO Logging
        self.connection.send_image_message(receiver, message_image, caption)

    def send_audio_message(self, receiver: str, message_audio: str, caption: str = "") -> None:
        """
        Sends an audio file to the receiver, with an optional caption/title
        :param receiver: The receiver of the message
        :param message_audio: The audio file to be sent
        :param caption: The caption/title to be displayed along with the audio, defaults to an empty string
        :return: None
        """
        # TODO Logging
        self.connection.send_audio_message(receiver, message_audio, caption)

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        raise NotImplementedError()

    def background_process(self) -> None:
        """
        A method that should be run in the background if has_background_process is True

        :return: None
        """
        if not self.has_background_process:
            return
        else:
            raise NotImplementedError()

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Check if the received message is a valid command for this service

        :param message: the message to be checked
        :return: True if the message is a valid command, False otherwise
        """
        raise NotImplementedError()

    @staticmethod
    def get_description(language):
        """
        Method that returns the help description of the plugin in a particular language.
        If the selected language has no description, the string
        "No help available for this language"
        will be returned instead

        :param language: the language to be returned
        :return: the description in that language
        """
        try:
            return Service.help_description[language.lower()]
        except KeyError:
            return "No help available for this language"
