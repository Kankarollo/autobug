import subprocess
from .api_template import logger

class Amass_API():

    def __init__(self):
        self.path = "amass"

    def scan_subdomains(self, domains, passive=True, save_to_file=False):
        logger.info(f"Scanning subdomains with {self.path}......")
        command = [self.path,"enum", "-d", domains]
        if passive:
            command.insert(2,"-passive")
        if save_to_file:
            command.extend(["-o","amass.out"])

        response = str(subprocess.check_output(command).decode())
        response = response.split()

        logger.info(f"Scanning subdomains completed.")
        return response