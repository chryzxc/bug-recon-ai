import subprocess
import json
from pathlib import Path
import os

class WhatWebScanner:
    def __init__(self):
        self.base_path = "/whatweb/output"
        
    def scan(self, domain, output_dir="outputs"):
        output_file = Path(output_dir) / f"{domain}_whatweb.json"
        output_file.parent.mkdir(exist_ok=True)
        
        if output_file.exists():
            try:
                os.remove(output_file)
                print(f"[*] Deleted existing file: {output_file}")
            except OSError as e:
                print(f"[!] Error deleting file: {e}")
                return []
        
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{Path.cwd()}/{output_dir}:{self.base_path}",
            "recon-whatweb", domain, f"--log-json={self.base_path}/{output_file.name}"
        ]
        try:
            subprocess.run(cmd, check=True)
            return self._parse_results(output_file)
        except subprocess.CalledProcessError as e:
            print(f"[!] Whatweb failed: {e}")
            return []

    def _parse_results(self, output_file):
        if not output_file.exists():
            return []
        
        with open(output_file) as f:
            try:
                results = []
                data = json.load(f)
                for target in data:
                    for key,value in target['plugins'].items():
                        results.append({key: value['string'] if 'string' in value else "" })
                # return [{
                #     'url': target['target'],
                #     'technologies': [plug for plug in target['plugins'].keys()],
                #     'source': 'WhatWeb'
                # } for target in data]
                return results
            except (json.JSONDecodeError, KeyError) as e:
                print(f"[!] Error parsing results: {e}")
                return []