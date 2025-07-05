import subprocess
import json
from pathlib import Path
import os
from utils.log_util import LogType,logger
from utils.misc import without_https
import re

class WPScanner:
    def __init__(self):
        self.base_path = "/wpscan/output"
        self.module_name = "WPScan"
        
    def scan(self, domain: str, output_dir="outputs")-> list[str]:
        logger(LogType.INITIALIZE,self.module_name)
        formatted_domain = without_https(domain)
        print("WPSCAN DOMAIN",formatted_domain)
        output_file = Path(output_dir) / f"{formatted_domain}_wpscan.txt"
        output_file.parent.mkdir(exist_ok=True)
        # parts = domain.split('.')
        # is_subdomain_only = len(parts) == 2
        
        # if domain.startswith("https://") or is_subdomain_only == False:
           
        #     logger(LogType.INVALID_TARGET,self.module_name)
        #     return []
        
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
            "wpscanteam/wpscan","--url" ,domain, "--output", f"{self.base_path}/{output_file.name}"
        ]
        try:
            logger(LogType.SCANNING,self.module_name,target=domain)
            
            subprocess.run(cmd, check=True)
            return self._parse_results(output_file)
        except subprocess.CalledProcessError as e:
            logger(LogType.ERROR,self.module_name,error=e)
            return []
        

    def _parse_results(self, output_file) -> list[str]:
        if not output_file.exists():
            logger(LogType.OUTPUT_FILE_NOT_FOUND,self.module_name)
            return []
        logger(LogType.PARSING,self.module_name)
        
        sections = []
        current_section = []
        capture = False

        with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
            try:
                
                for line in f:
                   
                    if "Interesting Finding(s):" in line:
                        capture = True
                    if capture == False:
                        continue
                    # print("LINE",line)
                    if line.strip() == '' and len(current_section) > 0:
                        # print("current section", current_section)
                        sections.append('\n'.join(current_section).strip())
                        current_section = []
                    if '|' in line or '[+]' in line:

                        
                            
                            formatted_line = re.sub(r'\x1b\[32m\[\+\]', '', line)
                            formatted_line = line = re.sub(r']\x1b\[0m', '', formatted_line)
                            formatted_line = formatted_line.replace("\u001b[0m ","")
                            # print("LINE",line)
                            # sections.append(''.join(current_section).strip())
                            current_section.append(formatted_line.strip())
                    # current_section.append(line)

                # if current_section:
                    # sections.append(''.join(current_section).strip())  # Last section
                # print("Sections",sections)
                logger(LogType.COMPLETED,self.module_name)
                return sections
            except (json.JSONDecodeError, KeyError) as e:
                logger(LogType.PARSE_ERROR,self.module_name,error=e)
                return []
                