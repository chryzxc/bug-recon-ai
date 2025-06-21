import subprocess
import json
from pathlib import Path

class Sublist3rScanner:
    def __init__(self):
        self.base_path = "/sublister/output"
        
    def scan(self, domain, output_dir="outputs"):
        output_file = Path(output_dir) / f"{domain}_subdomains.json"
        output_file.parent.mkdir(exist_ok=True)
        
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{Path.cwd()}/{output_dir}:{self.base_path}",
            "recon-sublister",
            "-d", domain,
            "-o", f"{self.base_path}/{output_file.name}"
        ]
        
        try:
            subprocess.run(cmd, check=True)
            return self._parse_results(output_file)
        except subprocess.CalledProcessError as e:
            print(f"[!] Sublist3r failed: {e}")
            return []

    def _parse_results(self, output_file):
        if not output_file.exists():
            return []
        
        with open(output_file) as f:
            return [{"domain": line.strip(), "source": "Sublist3r"} 
                   for line in f if line.strip()]