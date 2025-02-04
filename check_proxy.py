import requests
import concurrent.futures
from fake_useragent import UserAgent

class ProxyChecker:
    def __init__(self):
        self.ua = UserAgent()
        self.working_proxies = []
        self.check_urls = [
            "http://ip-api.com/json/",
            "https://api.myip.com",
            "https://ipinfo.io/json"
        ]

    def check_proxy(self, proxy):
        try:
            proxies = {
                'http': proxy,
                'https': proxy
            }
            headers = {'User-Agent': self.ua.random}
            
            # Try multiple IP check services
            for url in self.check_urls:
                try:
                    response = requests.get(url, 
                                         proxies=proxies,
                                         headers=headers,
                                         timeout=10)
                    if response.status_code == 200:
                        print(f"Working Proxy: {proxy} | IP: {response.json()}")
                        return proxy
                except:
                    continue
                    
        except Exception as e:
            print(f"Failed Proxy: {proxy} | Error: {str(e)}")
        return None

    def load_and_check_proxies(self, proxy_file="proxy.txt", max_workers=10):
        # Load proxies from file
        with open(proxy_file, "r") as f:
            proxy_list = []
            for line in f:
                host, port, user, pwd = line.strip().split(":")
                proxy = f"http://{user}:{pwd}@{host}:{port}"
                proxy_list.append(proxy)

        # Check proxies concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(self.check_proxy, proxy_list)
            
            # Filter working proxies
            self.working_proxies = [proxy for proxy in results if proxy]
            
        # Save working proxies
        with open("working_proxies.txt", "w") as f:
            for proxy in self.working_proxies:
                f.write(f"{proxy}\n")
                
        return self.working_proxies

if __name__ == "__main__":
    checker = ProxyChecker()
    working = checker.load_and_check_proxies()
    print(f"\nTotal working proxies: {len(working)}")
