import sqlalchemy
import concurrent.futures
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
import time
with open('URL_book.txt','r') as f:
    r = f.read()
headers = {
    'Cookie':'customerid=192798681734WF3SWYnqw; app_ad_closed=0; __BWfp=c1510154327592x2b23da575; ai_user=6ocS7|2017-11-08T16:31:44.789Z; ASPSESSIONIDSQRRCTQQ=OPGJGLKBABDLBGNPJPPLNFMP; kingstone_=ovST/8ymQmB+fsDX26ywr2v/1TI0000; _ga=GA1.3.2067812324.1510154327; _gid=GA1.3.699490028.1510154327; _gat=1; MyCount=0; MyAmt=0; NSC_xxx_mc*80=ffffffffaf181c1d45525d5f4f58455e445a4a423660; ai_session=fTM9|1510192668569.5|1510192668569.5',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
}
engine = sqlalchemy.create_engine("mysql+pymysql://root:0000@127.0.0.1:3306/?charset=utf8mb4")
engine.execute("CREATE DATABASE books_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")

URLS = r.strip("[]").replace('"','').split(",")

def load_url(url):
    req = urllib.request.Request(url,headers = headers)
    resp = urllib.request.urlopen(req)
    # urllib.request.urlopen(url, timeout=60) as conn:
    respData = str(resp.read().decode('utf-8'))  # 將所得的資料解碼
    soup = BeautifulSoup(respData,'lxml')

    book_names = soup.select('div.row_list > ul > li > a.anchor > span')
    authors = soup.select('div.row_list > ul > li > span.author')
    publishers = soup.select('div.row_list > ul > li > span.publisher')
    tags = soup.select('div#breadCrumb > a')
    book_list = []
    for i in range(0, 19):
        book = {}
        book['bookname'] = book_names[i].text
        print(book_names[i].text)
        book['author'] = authors[i].text
        book['publisher'] = publishers[i].text

        book['tag'] = tags[0].text + '>' + tags[1].text + '>' + tags[2].text + '>' + tags[3].text + '>' + tags[4].text
        book_list.append(book)


    df = pd.DataFrame(book_list)
    df.to_sql('kingstonebooks_test', engine, if_exists='append', schema='books_test', index=False)
# We can use a with statement to ensure threads are cleaned up promptly
def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(load_url, URLS)
if __name__ == '__main__':
    t_s = time.time()
    main()
    t_e = time.time()
    print(t_e-t_s)