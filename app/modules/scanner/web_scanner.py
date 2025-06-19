import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class WebScanner:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Toolkit/1.0'
        })
        self.visited = set()
    
    def crawl(self):
        to_visit = [{"url": self.target_url, "crawled_from": [self.target_url]}]
        discovered = []
    
        # while to_visit and len(self.visited) < max_pages:
        while len(to_visit) > 0:
            first_item = to_visit.pop(0)
            if first_item['url'] not in  self.visited:
            
                try:
                    response = self.session.get(first_item['url'], timeout=5)
                    self.visited.add(first_item['url'])
                
                    soup = BeautifulSoup(response.text, 'html.parser')
                    discovered.append({
                        'url': first_item['url'],
                        'status': response.status_code,
                        'title': soup.title.string if soup.title else None,
                        'crawled_from': first_item['crawled_from']
                    })
                
                    # Find new links
                    for link in soup.find_all('a', href=True):
                        print("LINK",link)
                        absolute_url = urljoin(first_item['url'], link['href'])
                        if absolute_url.startswith(self.target_url) and absolute_url not in self.visited:
                            crawled_from = [*first_item['crawled_from']]
                            if first_item['url'] != absolute_url:
                                crawled_from.append(absolute_url)
                            to_visit.append({"url":absolute_url,"crawled_from": crawled_from})
        
                except requests.RequestException as e:
                    print(f"Error scanning {first_item['url']}: {e}")
                
        return discovered