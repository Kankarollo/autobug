import subprocess
from .api_template import logger

class Httpx_API():
    
    def __init__(self):
        self.path = "httpx"

    def scan_from_file(self,filename):
        logger.info(f"Scanning subdomains with {self.path}......")

        command = [self.path, "-o", "httpx.out"]
        command.insert(1,filename)
        response = str(subprocess.check_output(command).decode())
        
        logger.info(f"Scanning subdomains with {self.path} completed.")