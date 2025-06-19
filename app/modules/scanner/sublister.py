import subprocess
import json
from pathlib import Path

class Sublist3rScanner:
    def scan(self, domain, output_dir="outputs"):
        output_file = Path(output_dir) / f"{domain}_subdomains.json"
        output_file.parent.mkdir(exist_ok=True)
        
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{Path.cwd()}/{output_dir}:/output",
            "recon-sublister",
            "-d", domain,
            "-o", f"/output/{output_file.name}"
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