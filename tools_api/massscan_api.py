import subprocess
from .api_template import logger

class Massscan_API():
    
    def __init__(self):
        self.path = "massscan"

    def scan_from_file(self,filename):
        logger.info(f"Scanning subdomains with {self.path}......")

        # command = [self.path,"-l",filename,"-status-code","-content-length","-title", "-tech-detect","-follow-redirects","-no-color","-ports", "80,443,8443,8080,8000","-o","httpx.out"]
        # response = str(subprocess.check_output(command).decode())

        logger.info(f"Scanning subdomains with {self.path} completed.")
        # print(response)
        # return response

    def scan_subdomain(self,subdomain):
        pass