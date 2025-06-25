import subprocess
import json
from pathlib import Path
import os

class NucleiScanner:
    def __init__(self):
        self.base_path = "/nuclei/output"
        
    def scan(self, domain, output_dir="outputs"):
        output_file = Path(output_dir) / f"{domain}_nuclei.txt"
        output_file.parent.mkdir(exist_ok=True)
        
        full_domain = domain if domain.startswith("https://") else f"https://{domain}"
        
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
            "projectdiscovery/nuclei","-target" ,full_domain, "--output", f"{self.base_path}/{output_file.name}"
        ]
        try:
            subprocess.run(cmd, check=True)
            return self._parse_results(output_file)
        except subprocess.CalledProcessError as e:
            print(f"[!] Nuclei failed: {e}")
            return []

    def _parse_results(self, output_file):
        if not output_file.exists():
            return []
      
   
        with open(output_file) as file:
            try:
                results = []
                for line in file:
                    results.append(line)
                return results
            except (json.JSONDecodeError, KeyError) as e:
                print(f"[!] Error parsing results: {e}")
                return []