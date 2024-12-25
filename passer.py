#!/usr/bin/python
from flagser import *
from sys import platform
import getpass
import pyperclip
import hashlib
import os

length = 25
password = ""
should_print = False
should_copy = True
config_path = "~/.config/passer"

def genPassword(pas):
    return hashlib.sha256(pas.encode()).hexdigest()

def setLen(arg):
    global length
    length = int(arg[0])
def setPass(arg):
    global password
    password = (arg[0])
def setPrint(arg):
    global should_print
    should_print = True if len(arg) < 1 else int(arg[0]) == 1
def setCopy(arg):
    global should_copy
    should_copy = True if len(arg) < 1 else int(arg[0]) == 1

def setSalt(args):
    path = os.path.expanduser(config_path) if platform == "linux" or platform == "linux2" or platform == "darwin" else "NEEDS A PATH IN WiNdoWs aka spy os"
    print(path)
    if os.path.isfile(path):
        with open(path,"w") as file:
            file.write(args[0])
    else:
        with open(path,"x") as file:
            file.write(args[0])

def getSalt():
    path = os.path.expanduser(config_path) if platform == "linux" or platform == "linux2" or platform == "darwin" else "NEEDS A PATH IN WiNdoWs aka spy os"
    if not os.path.exists(path):
        with open(path, 'w'): pass

    with open(path,"r") as file:
        return file.read()

def saltPassword(password):
    return password+getSalt()

m = FlagManager([
    Flag("-l","--length", description="specify length of password", onCall=lambda x : setLen(x)),
    Flag("-i","--in", description="password as arg", onCall=setPass),
    Flag("-p","--shouldprint", description="print password 1/0  (false default)", onCall=setPrint),
    Flag("-c","--shouldcopy", description="copy to clip board 1/0 (true default)", onCall=setCopy),
    Flag("-s","--setsalt", description="sets a salt (./config/passer)", onCall=setSalt),
    Flag("-gs","--getsalt", description="outputs the saved salt (./config/passer)", onCall=lambda x : print(getSalt())),
    Flag("-cs","--clearsalt", description="clears the saved salt (./config/passer)", onCall=lambda x : setSalt([""])),
])
m.description="passer is a program that will create a secure password from your input\n passer [command] [options]"
m.check()

if password == "" and ("-h" not in sys.argv and "-s" not in sys.argv and "-gs" not in sys.argv and "-cs" not in sys.argv):
    password = getpass.getpass("write your password: ")

pas = genPassword(saltPassword(password))[0:length]
if should_print:
    print(pas)

if should_copy:
    pyperclip.copy(pas)
