import subprocess
import json
from pathlib import Path
import os
from utils.log_util import LogType,logger
from utils.misc import without_https
class SubfinderScanner:
    def __init__(self):
        self.base_path = "/subfinder/output"
        self.module_name = "Subfinder"
        
    def scan(self, domain:str, output_dir="outputs")-> list[str]:
        logger(LogType.INITIALIZE,self.module_name)
        formatted_domain = without_https(domain)
        
        output_file = Path(output_dir) / f"{formatted_domain}_subfinder.txt"
        output_file.parent.mkdir(exist_ok=True)
        parts = domain.split('.')
        is_subdomain_only = len(parts) == 2
        
        if domain.startswith("https://") or is_subdomain_only == False:
           
            logger(LogType.INVALID_TARGET,self.module_name)
            return []
        
        if output_file.exists():
            try:
                os.remove(output_file)
                # print(Fore.GREEN + f"[Subfinder] Deleted existing file: {output_file}" + Style.RESET_ALL)
            except OSError as e:
                # print(Fore.GREEN + f"[Subfinder] Error deleting file: {e}" + Style.RESET_ALL)
                return []
        
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{Path.cwd()}/{output_dir}:{self.base_path}",
            "projectdiscovery/subfinder","-d" ,domain, "-silent", "-o", f"{self.base_path}/{output_file.name}"
        ]
        try:
            logger(LogType.SCANNING,self.module_name,target=domain)
            
            subprocess.run(cmd, check=True)
            return self._parse_results(output_file)
        except subprocess.CalledProcessError as e:
            logger(LogType.ERROR,self.module_name,error=e)
            return []

    def _parse_results(self, output_file):
        if not output_file.exists():
            logger(LogType.OUTPUT_FILE_NOT_FOUND,self.module_name)
            return []
        logger(LogType.PARSING,self.module_name)
   
        with open(output_file) as file:
            try:
                results = []
                for line in file:
                    results.append(line)
                logger(LogType.COMPLETED,self.module_name)
                return results
            except (json.JSONDecodeError, KeyError) as e:
                logger(LogType.PARSE_ERROR,self.module_name,error=e)
                return []