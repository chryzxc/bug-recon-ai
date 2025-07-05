from pathlib import Path
import sys
import os

from modules.scanner.wpscan import WPScanner
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from dotenv import load_dotenv
# load_dotenv()
import argparse
from modules.scanner.web_scanner import WebScanner
from modules.scanner.port_scanner import PortScanner
from modules.analyzer.vulnerability_analyzer import VulnerabilityAnalyzer
from modules.reporting.report_generator import ReportGenerator
from modules.ai.summarizer import AISummarizer
import json
from datetime import datetime
from modules.scanner.sublister import Sublist3rScanner
from modules.scanner.nmap import NmapScanner
from modules.scanner.whatweb import WhatWebScanner
from modules.analyzer.nuclei import NucleiScanner
from modules.scanner.subfinder import SubfinderScanner
from modules.scanner.katana import KatanaScanner
from colorama import Fore, Style

def main():
    
    # Initialize scanners
    parser = argparse.ArgumentParser(description="Bug Recon AI Toolkit")
    parser.add_argument("target", help="Target URL or IP address to scan")
    parser.add_argument("--output", help="Output directory for reports", default="reports")
    args = parser.parse_args()
    print(Fore.CYAN + f"Starting scan of {args.target}..." + Style.RESET_ALL)
    # Ensure output directory exists
    os.makedirs(args.output, exist_ok=True)
    
    print(Fore.CYAN + f"Loading modules..." + Style.RESET_ALL)
    # Initialize components
    web_scanner = WebScanner(args.target)
    # sub_scanner = Sublist3rScanner()
    nmap_scanner = NmapScanner()
    # output_file = Path("outputs") / f"nmap_elederm.ph.xml"
    # results = nmap_scanner._parse_results(output_file)
    # print("results",results)
    # return
    
    whatweb_scanner = WhatWebScanner()
    # port_scanner = PortScanner()
    vuln_analyzer = VulnerabilityAnalyzer()
    nuclei_scanner = NucleiScanner()
    subfinder_scanner = SubfinderScanner()
    report_gen = ReportGenerator()
    ai_summarizer = AISummarizer()
    katana_scanner = KatanaScanner()
   
    # Perform scans
    # web_pages = web_scanner.crawl()
    whatweb_results = whatweb_scanner.scan(args.target)
    nuclei_results = nuclei_scanner.scan(args.target)
    subdomains= subfinder_scanner.scan(args.target)
    crawled_pages = katana_scanner.scan(args.target)
    ports = nmap_scanner.scan(args.target)
    
    wps_result = []
    if any("WordPress" in result for result in whatweb_results):
        print(Fore.CYAN + "Wordpress detected..." + Style.RESET_ALL)
        wps_scanner = WPScanner()
        wps_result = wps_scanner.scan(args.target)
    
    # print("Scanning ports...")
    # port_results = port_scanner.scan(args.target)
    
    # Analyze findings
    # print("Analyzing for vulnerabilities...")
    findings = []
    # crawled_pages =[]
    # # Analyze web content
    # for page in web_pages:
    #     crawled_pages.append(page['url'])
        # page_findings = vuln_analyzer.analyze_web_content(str(page))
        # for finding in page_findings:
        #     finding['source'] = page['url']
        #     finding['crawled_from'] = page['crawled_from']
        #     findings.append(finding)
    
    # Sublist3r
    # print(f"Running Sublist3r on {args.target}")
    # subdomains = sub_scanner.scan(domainOnly(args.target), args.output)
    # print(f"[+] Found {len(subdomains)} subdomains")

    # 2. Port scanning
    # scan_targets = [args.target] + [sub['domain'] for sub in subdomains]
    all_ports = []
    
    # for target in scan_targets:
    #     print(f"[*] Scanning {target} with Nmap")
    #     ports = nmap_scanner.scan(domainOnly(target), output_dir=args.output)
    #     all_ports.extend(ports)
    #     print(f"[+] Found {len(ports)} open ports on {target}")
    
    # Analyze service versions
    # for host in port_results:
    #     for proto, ports in host['protocols'].items():
    #         for port_info in ports:
    #             cves = vuln_analyzer.match_versions(port_info)
    #             if cves:
    #                 findings.append({
    #                     'type': 'known_vulnerability',
    #                     'severity': 'critical',
    #                     'description': f"Known CVEs for {port_info['product']} {port_info['version']}",
    #                     'details': cves,
    #                     'source': f"{host['host']}:{port_info['port']}/{proto}"
    #                 })
    
    # # Generate AI summary
    # print("Generating AI summary...")
    # summary = ai_summarizer.summarize_findings(findings)
    summary = ai_summarizer.summarize_findings({
        'target': args.target,
        'scan_date': datetime.now().isoformat(),
        'findings': [*nuclei_results,*wps_result],
        'crawled_pages':crawled_pages,
        'ports':ports,
        'subdomains':subdomains,
        'technologies':whatweb_results})
    
    # Prepare final results
    scan_results = {
        'target': args.target,
        'scan_date': datetime.now().isoformat(),
        'findings': [*nuclei_results,*wps_result],
        'crawled_pages':crawled_pages,
        'ports':ports,
        'subdomains':subdomains,
        'technologies':whatweb_results,
        'summary': summary,
        # 'stats': {
        #     'total_findings': len(findings),
        #     'critical': len([f for f in findings if f['severity'] == 'critical']),
        #     'high': len([f for f in findings if f['severity'] == 'high']),
        #     'medium': len([f for f in findings if f['severity'] == 'medium']),
        #     'low': len([f for f in findings if f['severity'] == 'low'])
        # }
    }
    
    # Generate reports
    print(Fore.CYAN + f"Generating reports..." + Style.RESET_ALL)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON report
    json_report_path = os.path.join(args.output, f"scan_results_{timestamp}.json")
    with open(json_report_path, 'w') as f:
        json.dump(scan_results, f, indent=2)
    
    # Generate PDF report
    # pdf_report_path = os.path.join(args.output, f"scan_report_{timestamp}.pdf")
    # report_gen.generate_pdf_report(scan_results, pdf_report_path)
    
    # Generate visualizations
    report_gen.generate_visualizations(findings, os.path.join(args.output, "visualizations"))
    
    print(Fore.CYAN + f"Reports saved to {args.output}" + Style.RESET_ALL)
    print(f"Summary:\n{summary}")

if __name__ == "__main__":
    main()