import argparse
from pyfiglet import Figlet
import logging
import re
import os
import difflib as dl

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

def mark_files_old(*args):
    for filename in args:
        filename_new,extension = os.path.splitext(filename)
        filename_new = filename_new + "_old" + extension
        os.rename(filename,filename_new)


def compare_reports(filename):
    filename_old,extension = os.path.splitext(filename)
    filename_old = filename_old + "_old" + extension
    difference_list = []
    if not os.path.exists(filename_old):
        return difference_list
    with open(filename,'r') as file:
        file_data_new = file.readlines()
        file_data_new.sort()
    with open(filename_old,'r') as file:
        file_data_old = file.readlines()
        file_data_old.sort()

    difference_list = [diff for diff in dl.context_diff(file_data_new, file_data_old)]
    return difference_list

    
def is_inputSafe(user_input):
    re_pattern = re.compile("^\w{3,}\.[a-z]{2,}$")
    return re_pattern.match(user_input)

def perform_github_subdomain_scan(domain,SCAN_DIR):
    github_scan = GithubSubdomain_API()
    github_result_path = os.path.join(SCAN_DIR,f"github_scan_{domain}.txt")
    github_scan.find_subdomains(domain, github_result_path)
    return github_result_path

def perform_amass_scan(domain, SCAN_DIR):
    amass_api = Amass_API()
    if not is_inputSafe(domain):
        print(f"Domain: '{domain}' has wrong format")
    else:
        amass_result_path = os.path.join(SCAN_DIR,f"amass_scan_{domain}.txt")
        amass_api.find_subdomains(domain,amass_result_path)
    return amass_result_path

def perform_httpx_scan(amass_result_path,domain, SCAN_DIR):
    httpx_api = Httpx_API()
    httpx_result_path = os.path.join(SCAN_DIR,f"httpx_scan_{domain}.txt")
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
    
    if parser.scan_domain:
        domain_arg = parser.scan_domain
        if os.path.isfile(domain_arg):
            with open(domain_arg,'r') as file:
                scan_title = domain_arg
                domain_list = file.read().split()
        else:
            domain_list = [domain_arg]
            scan_title = domain_arg.split(".")[0]
        SCAN_DIR = os.path.join(DATABASE_DIR,scan_title)
        if not os.path.exists(SCAN_DIR):
            os.mkdir(SCAN_DIR)
        for domain in domain_list:
            amass_result_path = perform_amass_scan(domain, SCAN_DIR)
            github_result_path = perform_github_subdomain_scan(domain, SCAN_DIR)
            subdomains_file_name = merge_files(domain, SCAN_DIR, amass_result_path, github_result_path)
            httpx_result = perform_httpx_scan(subdomains_file_name,domain,SCAN_DIR)
        difference_subdomain_list = compare_reports(subdomains_file_name)
        difference_httpx_list =  compare_reports(httpx_result)
        if len(difference_subdomain_list) > 0:
            logger.warning(f"There are differences in report:{subdomains_file_name}")
            diff_report_filename = "diff_report_subdomains.txt"
            diff_report_filename = os.path.join(SCAN_DIR,diff_report_filename)
            logger.warning(f"Difference report saved in {diff_report_filename}.")
            with open(diff_report_filename, 'w') as file:
                file.writelines(difference_subdomain_list)
        elif len(difference_httpx_list) > 0:
            logger.warning(f"There are differences in report:{httpx_result}")
            diff_report_filename = "diff_report_httpx.txt"
            diff_report_filename = os.path.join(SCAN_DIR,diff_report_filename)
            logger.warning(f"Difference report saved in {diff_report_filename}.")
            with open(diff_report_filename, 'w') as file:
                file.writelines(difference_httpx_list)
        else:
            logger.info("No changes found from previous scan.")
            mark_files_old(amass_result_path,github_result_path,subdomains_file_name,httpx_result)
    logger.info("Autobug ended successfully.")

def test():
    subdomains_file_name = ""
    httpx_result = ""
    subdomains_file_name = ""
    difference_subdomain_list = compare_reports(subdomains_file_name)
    difference_httpx_list =  compare_reports(httpx_result)
    if len(difference_subdomain_list) > 0:
        logger.warning(f"There are differences in report:{subdomains_file_name}")
        logger.warning(difference_subdomain_list)
    elif len(difference_httpx_list) > 0:
        logger.warning(f"There are differences in report:{httpx_result}")
        logger.warning(difference_httpx_list)

if __name__ == '__main__':
    if not os.environ.get("GITHUB_TOKEN"):
        logger.warning("No GITHUB_TOKEN set in env variables.")
    if not os.path.isdir(DATABASE_DIR):
        os.mkdir(DATABASE_DIR)
    f = Figlet(font='slant')
    print(f.renderText('AUTOBUG'))

    parser = argparse.ArgumentParser() 
    parser.add_argument("-s","--scan_domain", help="Scan domains with amass.", type=str)

    args = parser.parse_args()
    main(args)
