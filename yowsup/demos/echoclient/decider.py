# -*- coding: utf-8 -*-
from yowsup.demos.echoclient.responses.food import *
from yowsup.demos.echoclient.responses.it_related import *
from yowsup.demos.echoclient.responses.smileys import *

def decide(messageProtocolEntity):

    sentmessage = messageProtocolEntity.getBody()
    sentmessageMin = sentmessage.lower()
    sender = messageProtocolEntity.getFrom()
    sendername = adressbook(messageProtocolEntity.getFrom(False))
    decision = ["", sender, ""]

    print("recv: " + sendername + ": " + sentmessage.lower())

    # Instant text replies
    if "keks" in sentmessageMin or "cookie" in sentmessageMin: decision[0] = kekse()
    elif "kuchen" in sentmessageMin: decision[0] = kuchen()
    elif "wã¼rfel" in sentmessageMin or "wuerfel" in sentmessageMin: decision[0] = wuerfel()
    elif "ð" in sentmessageMin: decision[0] = happyTears()
    elif "ðð»" in sentmessageMin: decision[0] = middleFinger()

    #terminal commands
    elif "term: " in sentmessageMin and sendername.split(" ")[0] == "Hermann":
        decision[2] = sentmessageMin.split("term: ")[1]

    #Special Text commands
    elif sentmessageMin in ["die", "stirb", "killbot"]: decision[0] = "ð¨ð«"

    #Print to console
    if decision[0]: print("sent: " + sendername + ": " + decision[0])
    elif decision[2]: print("cmnd: " + decision[2])

    return decision


def adressbook(adress):
    if adress == "4915779781557-1418747022":    return "Land of the very Brave      "
    elif adress == "4917628727937-1448730289":  return "Bottesting                  "
    elif adress == "4917628727937":             return "Hermann                     "
    else: return adress

def sizeChecker(string):
    if len(string) > 500: return "Message too long to send"
    else: return string