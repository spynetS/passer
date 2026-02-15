#!/usr/bin/python
import argparse
from sys import platform
import getpass
import pyperclip
import hashlib
import os
import string
import sys

# Configuration
CONFIG_PATH = "~/.config/passer"

def get_config_path():
    if platform in ["linux", "linux2", "darwin"]:
        return os.path.expanduser(CONFIG_PATH)
    return "NEEDS A PATH IN WiNdoWs aka spy os"

def get_salt():
    path = get_config_path()
    if path.startswith("NEEDS"):
        return ""
        
    if not os.path.exists(path):
        try:
            with open(path, 'w'): pass
        except OSError:
            pass

    try:
        with open(path, "r") as file:
            return file.read()
    except OSError:
        return ""

def set_salt(salt_text):
    path = get_config_path()
    print(path)
    if path.startswith("NEEDS"):
        return

    mode = "w" if os.path.isfile(path) else "x"
    try:
        with open(path, mode) as file:
            file.write(salt_text)
    except OSError as e:
        print(f"Error saving salt: {e}")

def gen_password(pas, legacy=False, alphabet=string.ascii_lowercase):
    if legacy:
        return hashlib.sha256(pas.encode()).hexdigest()

    digest = hashlib.sha256(pas.encode()).digest()
    
    if not alphabet:
        return ""

    chars = [alphabet[byte % len(alphabet)] for byte in digest]
    return "".join(chars)

def main():
    parser = argparse.ArgumentParser(
        description="passer is a program that creates a secure, deterministic password from your input.",
        epilog="passer [command] [options]"
    )

    # Core arguments
    parser.add_argument("-l", "--length", type=int, default=25, 
                        help="Specify length of password (default: 25)")
    parser.add_argument("-i", "--in", dest="password", 
                        help="Provide password as argument")

    # Toggles (using nargs='?' to support optional 0/1 args like the original, e.g. -p 0)
    parser.add_argument("-p", "--shouldprint", nargs="?", const=1, type=int, default=0, 
                        help="Print password 0/1 (default: 0)")
    parser.add_argument("-c", "--shouldcopy", nargs="?", const=1, type=int, default=1, 
                        help="Copy to clipboard 0/1 (default: 1)")

    # Complexity flags
    parser.add_argument("-nu", "--noupper", action="store_true", 
                        help="Disable uppercase characters")
    parser.add_argument("-nd", "--nodigits", action="store_true", 
                        help="Disable digits")
    parser.add_argument("-ns", "--nospecial", action="store_true", 
                        help="Disable special characters")

    # Salt management
    parser.add_argument("-s", "--setsalt", help="Set a salt string")
    parser.add_argument("-gs", "--getsalt", action="store_true", help="Show the currently saved salt")
    parser.add_argument("-cs", "--clearsalt", action="store_true", help="Clear the saved salt")

    # Legacy mode
    parser.add_argument("-lg", "--legazy", action="store_true", 
                        help="Generates passwords with old hash (13c4155)")

    args = parser.parse_args()

    # Handle Salt Actions (Priority over password generation)
    if args.setsalt is not None:
        set_salt(args.setsalt)
        return
    if args.clearsalt:
        set_salt("")
        return
    if args.getsalt:
        print(get_salt())
        return

    # Build Alphabet
    alphabet = string.ascii_lowercase
    if not args.noupper:
        alphabet += string.ascii_uppercase
    if not args.nodigits:
        alphabet += string.digits
    if not args.nospecial:
        alphabet += string.punctuation

    # Get Password
    password = args.password
    if password is None:
        try:
            password = getpass.getpass("write your password: ")
        except KeyboardInterrupt:
            print()
            sys.exit(0)

    # Generate
    full_pass = password + get_salt()
    generated_pass = gen_password(full_pass, args.legazy, alphabet)[0:args.length]

    # Output
    if args.shouldprint:
        print(generated_pass)

    if args.shouldcopy:
        pyperclip.copy(generated_pass)

if __name__ == "__main__":
    main()
