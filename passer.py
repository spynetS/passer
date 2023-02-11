#!/usr/bin/python
from flagser import *
import getpass
import pyperclip
import hashlib

length = 25
password = ""
should_print = False
should_copy = True

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


m = FlagManager([
    Flag("-l","--length     ", description="specify length of password", onCall=lambda x : setLen(x)),
    Flag("-i","--in         ", description="password as arg", onCall=setPass),
    Flag("-p","--shouldprint", description="print password 1/0  (false default)", onCall=setPrint),
    Flag("-c","--shouldcopy ", description="copy to clip board 1/0 (true default)", onCall=setCopy),
])
m.description="passer is a program that will create a secure password from your input\n passer [command] [options]"
m.check()

if password == "" and "-h" not in sys.argv:
    password = getpass.getpass("write your password: ")

pas = genPassword(password)[0:length]
if should_print:
    print(pas)

if should_copy:
    pyperclip.copy(pas)
