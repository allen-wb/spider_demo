import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup

table = []


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text(encoding='gb18030')


async def parser(html):
    soup = BeautifulSoup.find(html, 'lxml')
    book_list = soup.find('ul', class_="bang_list clearfix bang_list_mode")('li')

    for book in book_list:
        info = book.find_all('div')

        # 获取每本畅销书的排名，名称，评论数，作者，出版社
        rank = info[0].text[0:-1]
        name = info[2].text
        comments = info[3].text.split('条')[0]
        author = info[4].text
        date_and_publisher = info[5].text.split()
        publisher = date_and_publisher[1] if len(date_and_publisher) >= 2 else ''

        print(rank, name, comments, author, publisher)


async def download(url):
    async with aiohttp.ClientSession() as session:
        html = fetch(session, url)
        await parser(html)


urls = ['http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-%d' % i for i in range(1, 26)]
print('#' * 50)
t1 = time.time()

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(download(urls)) for url in urls]
tasks = asyncio.gather(*tasks)

t2 = time.time()  # 结束时间
print('使用aiohttp，总共耗时：%s' % (t2 - t1))
print('#' * 50)
