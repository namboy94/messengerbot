# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsapp-bot.

    whatsapp-bot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsapp-bot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsapp-bot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsapp-bot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_media.protocolentities import ImageDownloadableMediaMessageProtocolEntity, \
    RequestUploadIqProtocolEntity, AudioDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_presence.protocolentities import PresenceProtocolEntity
from yowsup.layers.protocol_profiles.protocolentities import SetStatusIqProtocolEntity
from startup.config.PluginConfigParser import PluginConfigParser
from utils.encoding.Unicoder import Unicoder
from utils.logging.LogWriter import LogWriter
from utils.contacts.AddressBook import AddressBook
from plugins.PluginManager import PluginManager
import time
import logging
import sys
import os
import traceback

logger = logging.getLogger(__name__)


class BotLayer(YowInterfaceLayer):
    """
    The BotLayer class
    The layer component of the bot. Used to send and receive messages
    """

    # class variables
    DISCONNECT_ACTION_PROMPT = 0
    parallel_running = False
    plugin_manager = None
    muted = False

    @ProtocolEntityCallback("message")
    def on_message(self, message_protocol_entity):
        """
        Method run when a message is received
        :param message_protocol_entity: the message received
        :return: void
        """

        # Notify whatsapp that message was read
        self.toLower(message_protocol_entity.ack())
        self.toLower(message_protocol_entity.ack(True))

        # Cases in which responses won't trigger
        if not message_protocol_entity.getType() == 'text':
            return
        if message_protocol_entity.getTimestamp() < int(time.time()) - 200:
            return
        if AddressBook().isBlackListed(message_protocol_entity.getFrom(False)):
            return
        if AddressBook().isBlackListed(message_protocol_entity.getParticipant(False)):
            return

        try:
            message_protocol_entity = Unicoder.fixIncominEntity(message_protocol_entity)
            LogWriter.writeEventLog("recv", message_protocol_entity)
            response = self.plugin_manager.runPlugins(message_protocol_entity)

            if response:
                if not self.muted:
                    LogWriter.writeEventLog("sent", response)
                    response = Unicoder.fixOutgoingEntity(response)
                    self.toLower(response)
                else:
                    LogWriter.writeEventLog("s(m)", response)

        except Exception as e:
            trace = traceback.format_exc()
            exception = TextMessageProtocolEntity("Exception: " + str(e) + "\n" + trace + "\n",
                                                  to=message_protocol_entity.getFrom())
            exception_image = os.getenv("HOME") + "/.whatsapp-bot/images/exception.jpg"
            if not self.muted:
                LogWriter.writeEventLog("exep", exception)
                LogWriter.writeEventLog("imgs",
                                        TextMessageProtocolEntity(exception_image + " --- " + exception.getBody(),
                                                                  to=message_protocol_entity.getFrom(False)))
                self.send_image(message_protocol_entity.getFrom(False), exception_image, exception.getBody())
            else:
                LogWriter.writeEventLog("e(m)", exception)
                LogWriter.writeEventLog("i(m)",
                                        TextMessageProtocolEntity(exception_image + " --- " + exception.getBody(),
                                                                  to=message_protocol_entity.getFrom()))

    def plugin_manager_setup(self):
        """
        Sets up the plugin manager
        :return: void
        """
        if self.plugin_manager is None:
            self.plugin_manager = PluginManager(self)
            self.plugin_manager.setPlugins(PluginConfigParser().readPlugins())
            if not self.parallel_running:
                print("Starting Parallel Threads")
                PluginManager(self).startParallelRuns()
                self.parallel_running = True

    # YOWSUP SPECIFIC METHODS

    def __init__(self):
        """
        Constructor, can be expanded for more functionality
        :return: void
        """
        # Required by Yowsup
        super(BotLayer, self).__init__()
        YowInterfaceLayer.__init__(self)
        self.accountDelWarnings = 0
        self.connected = False
        self.username = None
        self.sendReceipts = True
        self.disconnectAction = self.__class__.DISCONNECT_ACTION_PROMPT
        self.credentials = None
        self.jidAliases = {}

        # Methods to run on start
        self.plugin_manager_setup()
        self.set_presence_name("Whatsapp-Bot")
        self.profile_set_status("I am a bot.")

    @ProtocolEntityCallback("receipt")
    def on_receipt(self, entity):
        """
        method run whenever a whatsapp receipt is issued
        :param entity: The receipt entity
        :return: void
        """
        self.toLower(entity.ack())

    # Todo get rid of the lambdas
    def send_image(self, number, path, caption=None):
        """
        Sends an image
        :param number: the receiver of the image
        :param path: the path to the image file
        :param caption: the caption to be shown
        :return: void
        """
        jid = self.alias_to_jid(number)
        entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE, filePath=path)
        success_fn = lambda success_entity, original_entity:\
            self.on_request_upload_result(jid, path, success_entity, original_entity, caption)
        error_fn = lambda error_entity, original_entity:\
            BotLayer.on_request_upload_error(jid, path, error_entity, original_entity)
        self._sendIq(entity, success_fn, error_fn)

    # Todo get rid of the lambdas
    def send_audio(self, number, path):
        """
        Sends an audio file
        :param number: the number of the receiver of the file
        :param path: the path to the audio file
        :return: void
        """
        jid = self.alias_to_jid(number)
        entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO, filePath=path)
        success_fn = lambda success_entity, original_entity:\
            self.on_request_upload_result(jid, path, success_entity, original_entity)
        error_fn = lambda error_entity, original_entity:\
            BotLayer.on_request_upload_error(jid, path, error_entity, original_entity)
        self._sendIq(entity, success_fn, error_fn)

    # TODO get rid of the lambdas
    def on_request_upload_result(self, jid, file_path, result_request_upload_iq_protocol_entity,
                                 request_upload_iq_protocol_entity, caption=None):
        """
        Method run when a media upload result is positive
        :param jid: the jid to receive the media
        :param file_path: the path to the media file
        :param result_request_upload_iq_protocol_entity: the result entity
        :param request_upload_iq_protocol_entity: the request entity
        :param caption: the media caption, if applicable
        :return: void
        """

        if request_upload_iq_protocol_entity.mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO:
            do_send_fn = self.do_send_audio
        else:
            do_send_fn = self.do_send_image

        if result_request_upload_iq_protocol_entity.isDuplicate():
            do_send_fn(file_path, result_request_upload_iq_protocol_entity.getUrl(), jid,
                       result_request_upload_iq_protocol_entity.getIp(), caption)
        else:
            # TODO Fix the shadowing problems
            success_fn = lambda file_path, jid, url: do_send_fn(file_path, url, jid,
                                                                result_request_upload_iq_protocol_entity.getIp(),
                                                                caption)
            media_uploader = MediaUploader(jid, self.getOwnJid(), file_path,
                                           result_request_upload_iq_protocol_entity.getUrl(),
                                           result_request_upload_iq_protocol_entity.getResumeOffset(), success_fn,
                                           BotLayer.on_upload_error, BotLayer.on_upload_progress, async=False)
            media_uploader.start()

    @staticmethod
    def on_request_upload_error(jid, path, error_request_upload_iq_protocol_entity,
                                request_upload_iq_protocol_entity):
        """
        Method run when a media upload result is negative
        :param jid: the jid to receive the media
        :param path: the file path to the media
        :param error_request_upload_iq_protocol_entity: the error result entity
        :param request_upload_iq_protocol_entity: the request entity
        :return: void
        """
        if error_request_upload_iq_protocol_entity and request_upload_iq_protocol_entity:
            logger.error("Request upload for file %s for %s failed" % (path, jid))

    @staticmethod
    def on_upload_error(file_path, jid, url):
        """
        Method run when an upload error occurs
        :param file_path: the file path of the file to upload
        :param jid: the jid of the receiver of the file
        :param url: the upload url
        :return: void
        """
        logger.error("Upload file %s to %s for %s failed!" % (file_path, url, jid))

    @staticmethod
    def on_upload_progress(file_path, jid, url, progress):
        """
        Method that keeps track of the upload process
        :param file_path: the file path of the media file
        :param jid: the jid of the receiver
        :param url: the whatsapp upload url
        :param progress: the current progress
        :return:void
        """
        if url:
            sys.stdout.write("%s => %s, %d%% \r" % (os.path.basename(file_path), jid, progress))
            sys.stdout.flush()

    def alias_to_jid(self, c_alias):
        """
        Turns an alias into a jid
        :param c_alias: the current alias
        :return: the jid
        """
        for alias, a_jid in self.jidAliases.items():
            if c_alias.lower() == alias.lower():
                return BotLayer.normalize_jid(a_jid)

        return BotLayer.normalize_jid(c_alias)

    @staticmethod
    def normalize_jid(number):
        """
        Normalizes a jid
        :param number: the number to be receive a normalized jid
        :return: the normalized jid
        """
        if '@' in number:
            return number
        elif "-" in number:
            return "%s@g.us" % number

        return "%s@s.whatsapp.net" % number

    def do_send_image(self, file_path, url, to, ip=None, caption=None):
        """
        Sends an image file
        :param file_path: the path to the file
        :param url: the whatsapp upload url
        :param to: the receiver
        :param ip: the ip of the receiver
        :param caption: the caption to be displayed together with the image
        :return: void
        """
        entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(file_path, url, ip, to, caption=caption)
        self.toLower(entity)

    def do_send_audio(self, file_path, url, to, ip=None):
        """
        Sends an audio file
        :param file_path: the path to the audio file
        :param url: the whatsapp upload url
        :param to: the receiver of the file
        :param ip: the ip of the receiver
        :return: void
        """
        entity = AudioDownloadableMediaMessageProtocolEntity.fromFilePath(file_path, url, ip, to)
        self.toLower(entity)

    def set_presence_name(self, name):
        """
        Sets the presence name of the bot
        :param name: the presence name to set
        :return: void
        """
        entity = PresenceProtocolEntity(name=name)
        self.toLower(entity)

    def profile_set_status(self, text):
        """
        Sets the profile status of the bot
        :param text:
        :return: void
        """
        def on_success(result_iq_entity, original_iq_entity):
            """
            Run when successful
            :param result_iq_entity: the result entity
            :param original_iq_entity: the original entity
            :return: void
            """
            if result_iq_entity and original_iq_entity:
                print()

        def on_error(error_iq_entity, original_iq_entity):
            """
            Run when the profile status change failed
            :param error_iq_entity: the error entity
            :param original_iq_entity: the original entity
            :return: void
            """
            if error_iq_entity and original_iq_entity:
                logger.error("Error updating status")

        entity = SetStatusIqProtocolEntity(text)
        self._sendIq(entity, on_success, on_error)
