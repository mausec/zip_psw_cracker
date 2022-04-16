#!/usr/bin/env python3
"""[
    This script will crackme zip password base on password list.
    Created by: Mausec
    ]
"""
###############################################################################
###############################################################################
#############################IMPORT_SECTION####################################
import logging
import zipfile
import zlib
import os
import signal
import sys
from threading import Thread
from colorama import Fore
###############################################################################
###############################################################################
#############################LOGGING_SECTION###################################
LOGFILE_NAME = "zip_debug.log"
logging.basicConfig(filename=LOGFILE_NAME,
                    filemode="a+",
                    level=logging.ERROR,
                    format="%(asctime)s:%(levelname)s:%(message)s",
                    datefmt="%m/%d/%Y %I:%M:%S %p")
###############################################################################
###############################################################################
#############################FUNCTION_SECTION##################################


def func_greet():
    """[Function for greeting.]"""
    print(Fore.GREEN + "*-*-" * 14 + "*")
    print("*-*-" * 14 + "*")
    print(Fore.RED + "*****Mausec ZipCracker*****".center(55))
    print(Fore.GREEN + "*-*-" * 14 + "*")
    print("*-*-" * 14 + "*")


def func_zip_cracker(zfile, password):
    """[Function for cracking zip password]"""
    try:
        password = bytes(password, "utf-8")
        zfile.extractall(pwd=password)
        print(Fore.YELLOW + " " * 14 +
              "Cracked Password: " + password.decode("utf-8"))
        STOP_LST.append("stopme")
    except RuntimeError:
        pass
    except zlib.error:
        pass
    except zipfile.BadZipFile:
        pass
    except ValueError as errmsg:
        logging.error(errmsg)


def func_main():
    """[Function for main script logic]"""
    # We validate the user input for zip and password file indeed exist.
    if os.path.isfile(ZIP_FNAME) and os.path.isfile(PASSWD_FNAME):
        # We create a zip file object with user supplied zipfile.
        #zip_file_obj = zipfile.ZipFile(ZIP_FNAME)
        with zipfile.ZipFile(ZIP_FNAME, mode="r") as zip_file_obj:
            # Reading the password file and generate a list with it's content.
            with open(PASSWD_FNAME, encoding="utf-8") as fileobj:
                password_list = [word.strip("\n")
                                 for word in fileobj.readlines()]
                # We do a for loop to iterate over the password list.
                for pwd in password_list:
                    if STOP_LST:
                        signal.signal(signal.SIGINT, signal_handler)
                        print(Fore.RED + " " * 14 + "Press Ctrl+C")
                        signal.pause()
                    # We define our threading function and it's arguments.
                    thr = Thread(target=func_zip_cracker,
                                 args=(zip_file_obj, pwd))
                    thr.daemon = True
                    thr.start()  # We start our threading function.
                    thr.join()


def signal_handler(signum, frame):
    """[Function used to assist me in exiting Thread.]"""
    print("\t\t ", signum)
    sys.exit(0)


###############################################################################
###############################################################################
#############################MAIN_SECTION######################################
# We display our greeting message.
func_greet()

ZIP_FNAME = input("Enter Zipfile path name to crack.\n")
PASSWD_FNAME = input("Enter Password file.\n")
STOP_LST = []

# Call Main function in a try/except to handle some errors
try:
    func_main()
except RuntimeError as err_msg:
    logging.error(err_msg)
except ValueError as err_msg:
    logging.error(err_msg)
except KeyboardInterrupt as err_msg:
    logging.error(err_msg)
