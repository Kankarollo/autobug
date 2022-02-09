import argparse
from ast import arg
from pyfiglet import Figlet
import tools_api
import logging
import re

from tools_api.amass_api import Amass_API

LOGGER_NAME = "autobug-logger"
logger = logging.getLogger(LOGGER_NAME)

logger.setLevel(logging.INFO)
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
fileHandler = logging.FileHandler(f"{LOGGER_NAME}.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

def is_inputSafe(user_input):
    re_pattern = re.compile("^\w{3,}\.[a-z]{2,}$")
    return re_pattern.match(user_input)

def main(parser:argparse.ArgumentParser):
    logger.info("Starting program...")
    if parser.scan_domain:
        domain = parser.scan_domain
        if not is_inputSafe(domain):
            print("Domain has wrong format")
            return -1
        amass_api = Amass_API()
        subdomains = amass_api.scan_subdomains(domain)
        print(subdomains)
    logger.info("Autobug ended successfully.")

if __name__ == '__main__':
    f = Figlet(font='slant')
    print(f.renderText('AUTOBUG'))

    parser = argparse.ArgumentParser() 
    parser.add_argument("-s","--scan_domain", help="Scan domains with amass.", type=str)

    args = parser.parse_args()
    main(args)
