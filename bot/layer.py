"""
@author Hermann Krumrey<hermann@krumreyh.com>

The layer component of the bot. Used to send and receive messages
"""
import time

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback

from bot.utils.emojicode import *
from bot.utils.logwriter import writeLogAndPrint
from plugins.PluginManager import PluginManager


class EchoLayer(YowInterfaceLayer):

    parallelRunning = False

    """
    Method run when a message is received
    @param: messageProtocolEntity - the message received
    """
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        #Notify whatsapp that message was read
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))

        if not messageProtocolEntity.getType() == 'text': return
        if messageProtocolEntity.getTimestamp() < int(time.time()) - 200: return

        messageProtocolEntity = fixEntity(messageProtocolEntity)

        writeLogAndPrint("recv", messageProtocolEntity)

        pluginManager = PluginManager(self, messageProtocolEntity)
        response = pluginManager.runPlugins()
        if not self.parallelRunning:
            print("Starting Parallel Threads")
            PluginManager(self).startParallelRuns()
            self.parallelRunning = True

        if response:
            writeLogAndPrint("sent", response)
            response = convertEntityToBrokenUnicode(response)
            self.toLower(response)

        """

        sender = messageProtocolEntity.getFrom()
        message = messageProtocolEntity.getBody()

        try:
            participant = messageProtocolEntity.getParticipant(False)
        except: participant = ""

        writeLogAndPrint("recv", getContact(sender), message)

        try:
            decision = GeneralDecider(message, sender, participant, self).decide()
            if decision:
                if len(decision.message) > 2500: decision.message = "Message too long to send"
        except Exception as e:
            print(str(e))
            decision = Decision("An exception occured", sender)

        if decision:
            if decision.message:
                time.sleep(random.randint(0, 3))
                writeLogAndPrint("sent", getContact(decision.sender), decision.message)
                #if group: decision.message = convertToBrokenUnicode(decision.message)
                self.toLower(TextMessageProtocolEntity(decision.message, to=decision.sender))
        """

    """
    method run whenever a whatsapp receipt is issued
    """
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())