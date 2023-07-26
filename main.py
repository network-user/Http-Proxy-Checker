import asyncio
import concurrent.futures
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

url = 'http://eth0.me/'

proxy = set()
plist = input('Enter the full proxy file name: ')
with open(plist, 'r') as f:
    lines = f.readlines()
    for line in lines:
        proxy.add(line.strip())

proxies = [{'http': "http://" + p} for p in proxy]

def proxycheck(proxy_dict):
    try:
        response = requests.get(url=url, proxies=proxy_dict, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        text = soup.get_text()
        print(f'Valid proxy: {text.strip()}')
        return proxy_dict
    except requests.RequestException as e:
        print(f"Error with proxy {proxy_dict}: {e}'\n")
        return None

async def check_proxies(proxies):
    valid_proxies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(executor, proxycheck, proxy) for proxy in proxies]
        for response in await asyncio.gather(*tasks):
            if response:
                valid_proxies.append(response)
    return valid_proxies

def main():
    valid_proxies = asyncio.run(check_proxies(proxies))
    with open('valid_proxies.txt', 'w') as f:
        for p in valid_proxies:
            pxl = list(p.values())[0]
            pxls = urlparse(pxl).netloc
            pxls = pxls.replace("https://", "").replace("http://", "")
            f.write(pxls + '\n')
        print('Results in save valid_proxies.txt')
if __name__ == "__main__":
    main()
