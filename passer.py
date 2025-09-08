#!/usr/bin/python
from flagser import *
from sys import platform
import getpass
import pyperclip
import hashlib
import os
import string

length = 25
password = ""
should_help = False
should_print = False
should_copy = True
upper = True
special_characters = True
digits = True
config_path = "~/.config/passer"

def genPassword(pas):
    digest = hashlib.sha256(pas.encode()).digest()
    chars = [alphabet[byte % len(alphabet)] for byte in digest]
    return "".join(chars)

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
def setUpper(arg):
    global upper
    upper = False if len(arg) < 1 else int(arg[0]) == 1
def setSpecial(arg):
    global special_characters
    special_characters = False if len(arg) < 1 else int(arg[0]) == 1
def setDigits(arg):
    global digits
    digits = False if len(arg) < 1 else int(arg[0]) == 1

def setHelp(arg):
    global should_help
    should_help = True if len(arg) < 1 else int(arg[0]) == 1

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
    Flag("-h","--help", description="Displays of list of possible flags (false default)", onCall=setHelp),
    Flag("-nu","--noupper", description="Disable uppercase characters (false default)", onCall=setUpper),
    Flag("-nd","--nodigits", description="Disable digits (false default)", onCall=setDigits),
    Flag("-ns","--nospecial", description="Disable specialcase characters (false default)", onCall=setSpecial),
    Flag("-c","--shouldcopy", description="copy to clip board 1/0 (true default)", onCall=setCopy),
    Flag("-s","--setsalt", description="sets a salt (./config/passer)", onCall=setSalt),
    Flag("-gs","--getsalt", description="outputs the saved salt (./config/passer)", onCall=lambda x : print(getSalt())),
    Flag("-cs","--clearsalt", description="clears the saved salt (./config/passer)", onCall=lambda x : setSalt([""])),
])
m.description="passer is a program that will create a secure password from your input\n passer [command] [options]"
m.check()

if should_help:
    print("""passer is a program that creates a secure, deterministic password from your input.\n
You provide a master password (via -i or prompt), and passer combines it with a salt\n
to generate a reproducible hash-based password.

Usage:
  passer [options]

Options:
  -l, --length <n>        Specify length of the generated password (default: 25)
  -i, --in <password>     Provide password as argument instead of interactive prompt
  -p, --shouldprint [0/1] Print generated password (default: on)
  -c, --shouldcopy [0/1]  Copy generated password to clipboard (default: on)

  -nu, --noupper          Disable uppercase characters in the password
  -nd, --nodigits         Disable digits in the password
  -ns, --nospecial        Disable special characters in the password

  -s,  --setsalt <text>   Set a salt string (saved in ~/.config/passer)
  -gs, --getsalt          Show the currently saved salt
  -cs, --clearsalt        Clear the saved salt

  -h, --help              Show this help message and exit""")
    exit()

alphabet = string.ascii_lowercase 

if upper:
    alphabet += string.ascii_uppercase
if digits:
    alphabet += string.digits 
if special_characters:
    alphabet += string.punctuation

if password == "" and ("-h" not in sys.argv and "-s" not in sys.argv and "-gs" not in sys.argv and "-cs" not in sys.argv):
    password = getpass.getpass("write your password: ")

pas = genPassword(saltPassword(password))[0:length]
if should_print:
    print(pas)

if should_copy:
    pyperclip.copy(pas)
