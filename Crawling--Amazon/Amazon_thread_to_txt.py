import concurrent.futures
import requests
from bs4 import BeautifulSoup
import time
import json
with open('Literature_Fiction_EachPage_URL.txt','r') as f:
    r = f.read()
headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'skin=noskin; x-wl-uid=1zMzzqZcizh1dmp8sl8XFTcG9/6mzlrQsFu1pQWw+CCmJgS2bigQUAmeYbqsA83YRTmXByCzzkaM=; session-token=bpfH2ecjliQvHsbFqv81g2p17YGslUB9ssIUKVJx/6viNetOv1r71Ad9e8Ql+IcA3wGFG3IChYzEo7jxPTNgHxt0DXo/i5+LCKU/KySNDtLMT56DxDam7xshBFEBqnfwOxLo/abxV9sIezvNEo9w1ZHC0I6TzvhMMCQ/2B+QxpiR1YkFzt+wdr8qOsg0MLGuI4k0ZuTfqNozE97cqN/aJO0zEI79uznGVfF688L/vkyfEJUFFpBip73KH/9owigp; csm-hit=s-MYYJFT9X1HN3BGVS2XB4|1510761438103; ubid-main=132-0119528-4735475; session-id-time=2082787201l; session-id=146-9812624-9766246',
    'Host':'www.amazon.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}


URLS = r.strip("[]").replace('"','').split(",")
books_detail_URL = []
def load_url(url):
    resp = requests.get(url,headers = headers)
    soup = BeautifulSoup(resp.text,'html5lib')
    selects = soup.select(" div.a-fixed-left-grid-col > div.a-spacing-small > div.a-spacing-none > a")
    for s in selects:
        get = s.get("href")
        print(get)
        books_detail_URL.append(get)

# We can use a with statement to ensure threads are cleaned up promptly
def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for data in executor.map(load_url, URLS):
            with open("Books_detail_URL.txt", "w") as f:
                f.write(json.dumps(books_detail_URL))

if __name__ == '__main__':
    t_s = time.time()
    main()
    t_e = time.time()
    print(t_e-t_s)