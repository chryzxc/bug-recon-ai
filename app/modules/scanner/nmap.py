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
            "instrumentisto/nmap","-T4" ,"-n", "-Pn", "--top-ports", "100",
            "-sV", "--script=vuln",
            "-oX", f"/output/{output_file.name}",
            target
        ]
        
        try:
            subprocess.run(cmd, check=True)
            return self._parse_results(output_file)
        except subprocess.CalledProcessError as e:
            print(f"[!] Nmap scan failed: {e}")
            return []
        
    def get_elem_text(self,root, key):
        elem = root.find(f".//elem[@key='{key}']")
        return elem.text if elem is not None and elem.text is not None else "N/A"


    def _parse_results(self, xml_file):
        if not xml_file.exists():
            return []
            
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # results = []
        # for host in root.findall('host'):
        #     addr = host.find('address').get('addr')
        #     for port in host.findall('ports/port'):
        #         service = port.find('service')
        #         results.append({
        #             'host': addr,
        #             'port': port.get('portid'),
        #             'protocol': port.get('protocol'),
        #             'service': service.get('name'),
        #             'version': service.get('version', 'unknown'),
        #             'banner': service.get('product', '')
        #         })
        # return results
        
        results = []
        for port in root.findall(".//port"):
            port_data = {
                "port": port.get("portid"),
                "protocol": port.get("protocol"),
                "state": port.find("state").get("state"),
                "service": {
                    "name": port.find("service").get("name"),
                    "product": port.find("service").get("product", ""),
                    "version": port.find("service").get("version", ""),
                    "cpe": [cpe.text for cpe in port.findall("service/cpe")]
                },
                "vulnerabilities": []
            }
            # print("Scripts",port.find("script").get("name", ""))
            vuln_scripts = port.findall(".//script")
            
            for script in vuln_scripts:
                for table in script.findall(".//table"):
                   
                    # for elem in table.findall(".//elem"):
                    #     print("ELEM TEXT",elem.text)
                        
                    # print("TABLE",table)
                    
                    
                    vuln = {
                        "id": self.get_elem_text(table,"id"),
                        # "is_exploit": table.find("elem[@key='is_exploit']").text == 'true',
                        "type":self.get_elem_text(table,"type"),
                        "is_exploit":self.get_elem_text(table,"is_exploit") =='true'
                    }
                    # print("VULN",vuln)
                    port_data["vulnerabilities"].append(vuln)
                    
                
                
            
            # # Extract Vulners script output (CVEs/exploits)
            # vulners_script = port.find(".//script[@id='vulners']")
            # if vulners_script is not None:
            #     for table in vulners_script.findall("table/table"):
            #         vuln = {
            #             "type": table.find("elem[@key='type']").text,
            #             "id": table.find("elem[@key='id']").text,
            #             "is_exploit": table.find("elem[@key='is_exploit']").text == "true",
            #             "cvss": float(table.find("elem[@key='cvss']").text)
            #         }
            #         port_data["vulnerabilities"].append(vuln)
        
            results.append(port_data)
            
        # print("results",results)
    
        return results