import concurrent.futures
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
import time
with open('URL_tech.txt','r') as f:
    r = f.read()
URLS = r.strip("[]").replace('"','').split(",")
pd_list=[]
def load_url(url):
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    # urllib.request.urlopen(url, timeout=60) as conn:
    respData = str(resp.read().decode('utf-8'))  # 將所得的資料解碼
    soup = BeautifulSoup(respData,'lxml')

    news = {}
    news['Title'] = soup.select('div.column > h1')[0].text
    news['Datetime'] = soup.select('span.cnnDateStamp ')[0].text
    content_list = []
    select3 = soup.select('#storytext > p')
    for i in select3:
        content_list.append(i.text)
    news['Contents'] = content_list

    pd_list.append(news)


# We can use a with statement to ensure threads are cleaned up promptly
def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for data in executor.map(load_url, URLS):
            df = pd.DataFrame(pd_list)
            df.to_csv("CNNNEWSwithThread.csv")


if __name__ == '__main__':
    t_s = time.time()
    main()
    t_e = time.time()
    print(t_e-t_s)