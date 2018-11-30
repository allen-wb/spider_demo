import time

import requests
from bs4 import BeautifulSoup

table = []


def download(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')

    book_list = soup.find('ul', class_='bang_list clearfix bang_list_mode')('li')
    for book in book_list:
        info = book.find_all('div')

        rank = info[0].text[0:-1]
        name = info[2].text
        comments = info[3].text.split('条')[0]
        author = info[4].text
        date_and_publisher = info[5].text.split()
        publisher = date_and_publisher[1] if len(date_and_publisher) >= 2 else ''

        table.append([rank, name, comments, author, publisher])
        print(rank, name, comments, author, publisher)


urls = ['http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-%d' % i for i in range(1, 36)]

print('#' * 50)
t1 = time.time()

for url in urls:
    download(url)

t2 = time.time()
print('使用一般方法,总共耗时: %s' % (t2 - t1))
