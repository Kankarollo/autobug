import argparse
from pyfiglet import Figlet
import logging
import re
import os

from tools_api.amass_api import Amass_API
from tools_api.httpx_api import Httpx_API

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE_DIR = os.path.join(ROOT_DIR,"database")
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

def perform_amass_scan(domain, scan_title):
    SCAN_DIR = os.path.join(DATABASE_DIR,scan_title)
    if not os.path.exists(SCAN_DIR):
         os.mkdir(SCAN_DIR)
    amass_api = Amass_API()
    domain_list = []
    if os.path.isfile(domain):
        with open(domain,'r') as file:
            domain_list = file.read().split()
    else:
        domain_list = [domain]
    amass_result = []
    for domain in domain_list:
        if not is_inputSafe(domain):
            print(f"Domain: '{domain}' has wrong format")
        else:
            amass_result.extend(amass_api.scan_subdomains(domain))
    amass_result_path = os.path.join(SCAN_DIR,f"amass_scan_{scan_title}.txt")
    with open(amass_result_path,'w') as file:
        result = "\n".join(amass_result)
        file.write(result)
    return amass_result_path

def perform_httpx_scan(amass_result_path, scan_title):
    httpx_api = Httpx_API()
    SCAN_DIR = os.path.join(DATABASE_DIR,scan_title)
    httpx_result = httpx_api.scan_from_file(amass_result_path)
    httpx_result_path = os.path.join(SCAN_DIR,f"httpx_scan_{scan_title}.txt")
    with open(httpx_result_path,'w') as file:
        file.write(httpx_result)

def main(parser:argparse.ArgumentParser):
    logger.info("Starting program...")
    scan_title = input("Give title of the scan: ")
    
    if parser.scan_domain:
        domain = parser.scan_domain
        amass_result_path = perform_amass_scan(domain, scan_title)
        httpx_result = perform_httpx_scan(amass_result_path,scan_title)
        
    logger.info("Autobug ended successfully.")

if __name__ == '__main__':
    if not os.path.isdir(DATABASE_DIR):
        os.mkdir(DATABASE_DIR)
    f = Figlet(font='slant')
    print(f.renderText('AUTOBUG'))

    parser = argparse.ArgumentParser() 
    parser.add_argument("-s","--scan_domain", help="Scan domains with amass.", type=str)

    args = parser.parse_args()
    main(args)
