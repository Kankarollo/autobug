import subprocess
from .api_template import logger

class Httpx_API():
    
    def __init__(self):
        self.path = "httpx"

    def scan_from_file(self,filename,output_filename):
        logger.info(f"Scanning subdomains with {self.path}......")

        command = [self.path,"-l",filename,"-status-code","-content-length","-title", "-tech-detect","-follow-redirects","-no-color","-ports", "80,443,8443,8080,8000","-o",output_filename]
        subprocess.check_output(command).decode()

        logger.info(f"Scanning subdomains with {self.path} completed.")

    def scan_subdomain(self,subdomain):
        pass