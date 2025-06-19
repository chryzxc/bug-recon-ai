import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

class NmapScanner:
    def scan(self, target, ports="1-1000", output_dir="outputs"):
        output_file = Path(output_dir) / f"nmap_{target.replace('/', '_')}.xml"
        output_file.parent.mkdir(exist_ok=True)
        
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{Path.cwd()}/{output_dir}:/output",
            "instrumentisto/nmap",
            "-sV", "-p", ports,
            "-oX", f"/output/{output_file.name}",
            target
        ]
        
        try:
            subprocess.run(cmd, check=True)
            return self._parse_results(output_file)
        except subprocess.CalledProcessError as e:
            print(f"[!] Nmap scan failed: {e}")
            return []

    def _parse_results(self, xml_file):
        if not xml_file.exists():
            return []
            
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        results = []
        for host in root.findall('host'):
            addr = host.find('address').get('addr')
            for port in host.findall('ports/port'):
                service = port.find('service')
                results.append({
                    'host': addr,
                    'port': port.get('portid'),
                    'protocol': port.get('protocol'),
                    'service': service.get('name'),
                    'version': service.get('version', 'unknown'),
                    'banner': service.get('product', '')
                })
        return results