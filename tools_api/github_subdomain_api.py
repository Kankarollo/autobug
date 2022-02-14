import subprocess,os
from .api_template import logger

class GithubSubdomain_API():
    
    def __init__(self):
        self.path = "github-subdomains"
        self.token = os.environ["GITHUB_TOKEN"]

    def find_subdomains(self,domain,output_filename):
        logger.info(f"Discovering subdomains with {self.path}......")

        filename = f"{domain}_github.txt"
        if not self.token:
            logger.error("No github token added. Scan won't be performed.")
            return
        command = [self.path,"-d",domain, "-t", self.token, "-o", output_filename]
        subprocess.check_output(command).decode()

        logger.info(f"Discovering subdomains with {self.path} completed.")
        # print(response)

    def scan_subdomain(self,subdomain):
        pass