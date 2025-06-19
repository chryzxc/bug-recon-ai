import nmap 

class PortScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()
    
    def scan(self, target, ports='1-1024', arguments='-sV'):
        """Perform port scanning with version detection"""
        print(f"Scanning {target} on ports {ports}...")
        self.nm.scan(hosts=target, ports=ports, arguments=arguments)
        
        results = []
        for host in self.nm.all_hosts():
            host_info = {
                'host': host,
                'status': self.nm[host].state(),
                'protocols': {}
            }
            
            for proto in self.nm[host].all_protocols():
                host_info['protocols'][proto] = []
                for port in self.nm[host][proto].keys():
                    service = self.nm[host][proto][port]
                    host_info['protocols'][proto].append({
                        'port': port,
                        'state': service['state'],
                        'service': service['name'],
                        'version': service.get('version', 'unknown'),
                        'product': service.get('product', 'unknown')
                    })
            
            results.append(host_info)
        
        return results