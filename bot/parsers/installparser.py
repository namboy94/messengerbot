import os
import platform

def isInstalled():

    if platform.system() == "Linux":
        homedir = os.getenv("HOME")
        if not os.path.isdir(homedir + "/.whatsapp-bot"): return False
        if not os.path.isdir(homedir + "/.whatsapp-bot/logs"): return False
        if not os.path.isdir(homedir + "/.whatsapp-bot/program"): return False
        if not os.path.isfile(homedir + "/.whatsapp-bot/config"): return False
        if not os.path.isfile("/usr/bin/whatsapp-bot"): return False
        return True

    elif platform.system() == "Windows":
        return False


def install():

    if platform.system() == "Linux":
        homedir = os.getenv("HOME")
        whatsappbotdir = homedir + "/.whatsapp-bot"
        programdir = whatsappbotdir + "/program"
        if not os.path.isdir(whatsappbotdir):
            os.system("mkdir " + whatsappbotdir)
        if not os.path.isdir(programdir):
            os.system("mkdir " + programdir)
            os.system("cp -rf ../ " + programdir)
        if not os.path.isdir(whatsappbotdir + "/logs"):
            os.system("mkdir " + whatsappbotdir + "/logs")
        if not os.path.isfile(whatsappbotdir + "/config"):
            file = open(whatsappbotdir + "/config", "w")
            file.write("number=\npassword=")
            file.close()
        if not os.path.isfile("/usr/bin/whatsapp-bot"):
            os.system("gksudo cp continuousscript /usr/bin/whatsapp-bot")
            os.system("gksudo chmod 755 /usr/bin/whatsapp-bot")

    elif platform.system() == "Windows":
        return False

def update():
    if platform.system() == "Linux":
        homedir = os.getenv("HOME")
        whatsappbotdir = homedir + "/.whatsapp-bot"
        programdir = whatsappbotdir + "/program"
        os.system("rm -rf " + programdir)
        os.system("cp -rf ../ " + programdir)
    elif platform.system() == "Windows":
        return False