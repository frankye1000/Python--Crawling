import sqlalchemy
import concurrent.futures
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
import time
with open('URL_news.txt','r') as f:
    r = f.read()
headers ={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
engine = sqlalchemy.create_engine("mysql+pymysql://root:fff810924@127.0.0.1:3306/?charset=utf8mb4")
# engine.execute("CREATE DATABASE news CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")

URLS = r.strip("[]").replace('"','').split(",")

def load_url(url):
    req = urllib.request.Request(url,headers = headers)
    resp = urllib.request.urlopen(req)
    # urllib.request.urlopen(url, timeout=60) as conn:
    respData = str(resp.read().decode('utf-8'))  # 將所得的資料解碼
    soup = BeautifulSoup(respData,'lxml')

    select1 = soup.select('h1.article-title')
    select2 = soup.select('div.article-info')
    select3 = soup.select('div.article-content > p')
    article = {}
    article['title'] = select1[0].text
    article['date'] = select2[0].text.strip().split(',')[0].strip()
    article['class'] = select2[0].text.split(',')[1].strip()
    pd_list=[]
    # content_list = []
    # for select in select3:  # 因為內容是字串所以只能用for來句句取出
    #     content_list.append(select.text)
    # article['content'] = content_list

    pd_list.append(article)
    df = pd.DataFrame(pd_list)
    df.to_sql('newscontentall', engine, if_exists='append', schema='news', index=False)
# We can use a with statement to ensure threads are cleaned up promptly
def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(load_url, URLS)
if __name__ == '__main__':
    t_s = time.time()
    main()
    t_e = time.time()
    print(t_e-t_s)