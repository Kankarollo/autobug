import argparse
import git
from pyfiglet import Figlet
import logging
import re
import os

from tools_api.amass_api import Amass_API
from tools_api.httpx_api import Httpx_API
from tools_api.github_subdomain_api import GithubSubdomain_API

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

def perform_github_subdomain_scan(domain,scan_title):
    SCAN_DIR = os.path.join(DATABASE_DIR,scan_title)
    github_scan = GithubSubdomain_API()
    github_result_path = os.path.join(SCAN_DIR,f"github_scan_{scan_title}.txt")
    github_scan.find_subdomains(domain, github_result_path)
    return github_result_path

def perform_amass_scan(domain, scan_title):
    SCAN_DIR = os.path.join(DATABASE_DIR,scan_title)
    if not os.path.exists(SCAN_DIR):
         os.mkdir(SCAN_DIR)
    amass_api = Amass_API()
    if not is_inputSafe(domain):
        print(f"Domain: '{domain}' has wrong format")
    else:
        amass_result_path = os.path.join(SCAN_DIR,f"amass_scan_{scan_title}.txt")
        amass_api.find_subdomains(domain,amass_result_path)
    return amass_result_path

def perform_httpx_scan(amass_result_path, scan_title):
    httpx_api = Httpx_API()
    SCAN_DIR = os.path.join(DATABASE_DIR,scan_title)
    httpx_result_path = os.path.join(SCAN_DIR,f"httpx_scan_{scan_title}.txt")
    httpx_api.scan_from_file(amass_result_path,httpx_result_path)
    return httpx_result_path

def merge_files(domain,output_dir,*args):
    final_data = []
    for filename in args:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                final_data.extend(file.readlines())
    length_before = len(final_data)
    final_data = set(final_data)
    cleared_lines = length_before - len(final_data)
    print(f"{cleared_lines} were filtered.")
    subdomains_file_name = os.path.join(output_dir,f"{domain}_subdomains.txt")
    with open(subdomains_file_name, 'w') as file:
        for line in final_data:
            file.write(line)
    return subdomains_file_name

def main(parser:argparse.ArgumentParser):
    logger.info("Starting program...")
    scan_title = input("Give title of the scan: ")
    SCAN_DIR = os.path.join(DATABASE_DIR,scan_title)
    
    if parser.scan_domain:
        domain = parser.scan_domain
        if not os.path.exists(SCAN_DIR):
            os.mkdir(SCAN_DIR)
        if os.path.isfile(domain):
            with open(domain,'r') as file:
                domain_list = file.read().split()
        else:
            domain_list = [domain]
        for domain in domain_list:
            amass_result_path = perform_amass_scan(domain, scan_title)
            github_result_path = perform_github_subdomain_scan(domain, scan_title)
            subdomains_file_name = merge_files(domain, SCAN_DIR, amass_result_path, github_result_path)

            httpx_result = perform_httpx_scan(subdomains_file_name,scan_title)
        
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
