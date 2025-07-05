import subprocess
import json
from pathlib import Path
import os
from app.utils.misc import without_https
from utils.log_util import LogType,logger
class WhatWebScanner:
    def __init__(self):
        self.base_path = "/whatweb/output"
        self.module_name = "Whatweb"
        
    def scan(self, domain, output_dir="outputs")-> list[dict]:
        logger(LogType.INITIALIZE,self.module_name)
        formatted_domain = without_https(domain)
        output_file = Path(output_dir) / f"{formatted_domain}_whatweb.json"
        output_file.parent.mkdir(exist_ok=True)
        
        if output_file.exists():
            try:
                os.remove(output_file)
                # print(Fore.GREEN + f"[Whatweb] Deleted existing file: {output_file}" + Style.RESET_ALL)
            except OSError as e:
                # print(Fore.GREEN + f"[Whatweb] Error deleting file: {e}" + Style.RESET_ALL)
                return []
        
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{Path.cwd()}/{output_dir}:{self.base_path}",
            "recon-whatweb", domain, "-q" , f"--log-json={self.base_path}/{output_file.name}"
        ]
        try:
            logger(LogType.SCANNING,self.module_name,target=domain)
            subprocess.run(cmd, check=True)
            return self._parse_results(output_file)
        except subprocess.CalledProcessError as e:
            logger(LogType.ERROR,self.module_name,error=e)
            
            return []
        
    def _parse_data(self,value):
        if 'string' in value:
            return value['string']
        if 'version' in value:
            return value['version']
        if 'module' in value:
            return value['module']
        return ""
        

    def _parse_results(self, output_file):
        if not output_file.exists():
            logger(LogType.OUTPUT_FILE_NOT_FOUND,self.module_name)
            return []
        
        with open(output_file) as f:
            try:
                results = []
                data = json.load(f)
                logger(LogType.PARSING,self.module_name)
                for target in data:
                    for key,value in target['plugins'].items():
                    
                        results.append({key: self._parse_data(value)})
                logger(LogType.COMPLETED,self.module_name)
                return results
            except (json.JSONDecodeError, KeyError) as e:
                logger(LogType.PARSE_ERROR,self.module_name,error=e)
                return []