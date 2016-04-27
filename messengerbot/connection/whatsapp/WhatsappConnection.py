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
import re
from typing import Tuple

from yowsup.layers.interface import YowInterfaceLayer
from yowsup.layers.interface import ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity

from messengerbot.connection.generic.Message import Message
from messengerbot.connection.generic.Connection import Connection
from messengerbot.connection.whatsapp.layers.YowsupEchoLayer import YowsupEchoLayer
from messengerbot.connection.whatsapp.stacks.YowsupEchoStack import YowsupEchoStack
from messengerbot.connection.whatsapp.yowsupwrapper.WrappedYowInterfaceLayer import WrappedYowInterfaceLayer
from messengerbot.connection.whatsapp.yowsupwrapper.entities.WrappedTextMessageProtocolEntity \
    import WrappedTextMessageProtocolEntity


class WhatsappConnection(WrappedYowInterfaceLayer, YowsupEchoLayer, Connection):
    """
    Class that implements the connection to the Whatsapp Messaging service
    """

    def __init__(self) -> None:
        """
        Constructor for the WhatsappConnection class that initializes the Yowsup layer

        :return: None
        """
        super().__init__()
        # noinspection PyCallByClass
        YowInterfaceLayer.__init__(self)

    def send_text_message(self, message: Message) -> None:
        """
        Sends a text message to the receiver. Some services allow the use of titles, but some don't,
        so the message title is optional
        :param message: The message to be sent
        :return: None
        """
        message_protocol_entity = self.convert_message_to_text_message_protocol_entity(message)
        self.to_lower(message_protocol_entity)

    def send_image_message(self, receiver: str, message_image: str, caption: str = "") -> None:
        """
        Sends an image to the receiver, with an optional caption/title
        :param receiver: The receiver of the message
        :param message_image: The image to be sent
        :param caption: The caption/title to be displayed along with the image, defaults to an empty string
        :return: None
        """
        self.send_image(receiver, message_image, caption)

    def send_audio_message(self, receiver: str, message_audio: str, caption: str = "") -> None:
        """
        Sends an audio file to the receiver, with an optional caption/title
        :param receiver: The receiver of the message
        :param message_audio: The audio file to be sent
        :param caption: The caption/title to be displayed along with the audio, defaults to an empty string
        :return: None
        """
        str(caption)
        self.send_audio(receiver, message_audio)

    @staticmethod
    def establish_connection(credentials: Tuple[str]) -> None:
        """
        Establishes the connection to the specific service

        :return: None
        """
        echo_stack = YowsupEchoStack(WhatsappConnection, credentials)
        echo_stack.start()

    @ProtocolEntityCallback("message")
    def on_message(self, message_protocol_entity: TextMessageProtocolEntity):
        """
        Method run when a message is received
        :param message_protocol_entity: the message received
        :return: void
        """
        # Wrap the message protocol entity in a PEP8-compliant Wrapper
        wrapped_entity = WrappedTextMessageProtocolEntity(entity=message_protocol_entity)
        message = self.convert_text_message_protocol_entity_to_message(wrapped_entity)
        self.on_incoming_message(message)

    @staticmethod
    def convert_text_message_protocol_entity_to_message(message_protocol_entity: WrappedTextMessageProtocolEntity) \
            -> Message:
        """
        Converts an incoming text message protocol entity into a Message object

        :param message_protocol_entity: The entity to convert
        :return: the converted message
        """
        body = message_protocol_entity.get_body()

        sender_number = message_protocol_entity.get_from(True)
        sender_identifier = message_protocol_entity.get_from(False)
        sender_name = message_protocol_entity.get_notify()
        group = False
        individual_number = ""
        individual_identifier = ""
        individual_name = ""

        if re.search(r"[0-9]+-[0-9]+", sender_identifier):
            group = True
            individual_number = message_protocol_entity.get_participant(True)
            individual_identifier = message_protocol_entity.get_participant(False)
            individual_name = message_protocol_entity.get_notify()

        return Message(body, "", sender_number, sender_identifier, sender_name, True, group,
                       individual_number, individual_identifier, individual_name)

    @staticmethod
    def convert_message_to_text_message_protocol_entity(message: Message) -> WrappedTextMessageProtocolEntity:
        """
        Converts an outgoing message object into a text message protocol entity

        :param message: The message to be converted
        :return: The converted text message protocol entity
        """
        to = message.address
        body = message.message_body

        return WrappedTextMessageProtocolEntity(body, to=to)