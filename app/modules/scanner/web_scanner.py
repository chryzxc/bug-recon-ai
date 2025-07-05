from colorama import Fore, Style
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils.log_util import logger,LogType
class WebScanner:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Toolkit/1.0'
        })
        self.visited = set()
        self.module_name="Web Scanner"
    
    def crawl(self):
        logger(LogType.INITIALIZE,self.module_name)
        to_visit = [{"url": self.target_url, "crawled_from": [self.target_url]}]
        discovered = []
        logger(LogType.CRAWLING,self.module_name,target=self.target_url)
    
        # while to_visit and len(self.visited) < max_pages:
        while len(to_visit) > 0:
            first_item = to_visit.pop(0)
            if first_item['url'] not in  self.visited:
            
                try:
                    full_domain = f"https://{first_item['url']}" if not first_item['url'].startswith("https://") else first_item['url']
                    response = self.session.get(full_domain, timeout=5)
                    self.visited.add(full_domain)
                
                    soup = BeautifulSoup(response.text, 'html.parser')
                    discovered.append({
                        'url': full_domain,
                        'status': response.status_code,
                        'title': soup.title.string if soup.title else None,
                        'crawled_from': first_item['crawled_from']
                    })
                
                    # Find new links
                    for link in soup.find_all('a', href=True):
                        print(Fore.GREEN + f"[{self.module_name}] Link discovered: {link['href']}" + Style.RESET_ALL)
                    
                        absolute_url =link['href'] if link['href'].startswith(full_domain) else urljoin(full_domain, link['href'])
                       
                        if self.target_url in absolute_url and absolute_url not in self.visited and absolute_url.startswith("https://"):
                            crawled_from = [*first_item['crawled_from']]
                            if full_domain != absolute_url:
                                crawled_from.append(absolute_url)
                            to_visit.append({"url":absolute_url,"crawled_from": crawled_from})
        
                except requests.RequestException as e:
                    logger(LogType.ERROR,self.module_name,error=e)
                    
                
        return discovered