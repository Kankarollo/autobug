import subprocess
from .api_template import logger

class Amass_API():

    def __init__(self):
        self.path = "amass"

    def find_subdomains(self, domains,amass_result_path, passive=True, save_to_file=True):
        logger.info(f"Discover subdomains with {self.path}......")
        command = [self.path,"enum", "-d", domains]
        if passive:
            command.insert(2,"-passive")
        if save_to_file:
            command.extend(["-o",amass_result_path])

        subprocess.check_output(command).decode()
        logger.info(f"Discovering subdomains completed.")