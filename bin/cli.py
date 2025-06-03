import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()
from core.recon.wapiti_scan import WapitiScanner
from core.recon.subdomain import SubdomainEnumerator
# from ai.summarizer import get_ai_summary
from colorama import Fore, Style
def main():
    # if len(sys.argv) != 2:
    #     print('args',len(sys.argv))
    #     print("Usage: python main.py <domain>")
    #     return

    domain = input("Enter domain (e.g., example.com): ")
    print(Fore.CYAN + f"🔍 Scanning {domain}..." + Style.RESET_ALL)
    enum = SubdomainEnumerator()
    subdomains = enum.enumerate(domain)
    print(Fore.GREEN + f"✅ Found {len(subdomains)} subdomains" + Style.RESET_ALL)
    
    scanner = WapitiScanner(domain)
    scanner.scan()
    # domain = sys.argv[1]


    # # subdomains = get_subdomains(domain)
    # print(f"\n[+] Found {len(subdomains)} subdomains:")
    # for s in subdomains:
    #     print(f" - {s}")

    
    

    # summary = get_ai_summary(subdomains)
    # print(Fore.YELLOW + "\n🧠 AI Summary:\n" + Style.RESET_ALL + summary)

if __name__ == "__main__":
    main()