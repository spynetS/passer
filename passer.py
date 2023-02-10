#!/usr/bin/python
from flagser import *
import getpass
from passlib.hash import argon2
import pyperclip

length = 25
password = ""
should_print = False
should_copy = True

def genPassword(pas):
    return argon2.using(rounds = 2, salt = bytes("Ckdxu0QBSYoNbnSW", 'utf-8'), parallelism = 1).hash(pas).split("=")[4].split("w$")[1]

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
    Flag("-l", description="specify length of password", onCall=lambda x : setLen(x)),
    Flag("-in", description="password as arg", onCall=setPass),
    Flag("-p", description="print password 1/0  (false default)", onCall=setPrint),
    Flag("-c", description="copy to clip board 1/0 (true default)", onCall=setCopy),
])

m.check()

fname = sys.argv[len(sys.argv)-1]
if password == "":
    password = getpass.getpass("write your password: ")

pas = genPassword(password)[0:length]
if should_print:
    print(pas)

if should_copy:
    pyperclip.copy(pas)
