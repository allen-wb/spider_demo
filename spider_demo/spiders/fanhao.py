import scrapy
from scrapy.http import Request
import requests


class FanHaoSpider(scrapy.Spider):
	name = 'fanhao'
	start_urls = ['https://www.mgsbuy.net']
	url = 'https://www.mgsbuy.net'

	# def start_requests(self):
	# 	urls = ['https://www.mgsbuy.net']
	#
	# 	# for url in urls:
	# 	# 	yield scrapy.Request(url, callback=self.parse)
	# 	for a in range(436):
	# 		if a > 0:
	# 			yield Request(self.url + '/page/' + str(a), callback=self.parse)  # 爬取到的页面如何处理？提交给parse方法处理

	def parse(self, response):
		# url_links = response.xpath("//div[@class='pagination']//@href").extract()
		# print('last=', url_links[len(url_links) - 1])
		# last_url = url_links[len(url_links) - 1]

		names = response.xpath("//div[@class='thumbnail boxx']//@href").extract()
		images = response.xpath("//div[@class='thumbnail boxx']//@src").extract()

		# for name in names:
		# 	with open("test.txt", 'a') as f:
		# 		f.write(name.split('/')[-1].split('.')[0])
		# 		f.write('\r')

		next_url = response.xpath("//div[@class='pagination']//a[@class='next']").extract()
		if next_url:
			url = next_url[0].split(r'"')[1]
			with open('text.txt', 'a') as f:
				f.write(url)
				f.write('\r')
			yield Request(url=url, callback=self.parse)

		# if next_url:
		# 	with open('text.txt', 'a') as f:
		# 		f.write(next_url[0])
		# 		f.write('\r')

		# re = requests.request('get', images[0])
		# with open('test.jpg', 'wb') as f:
		# 	f.write(re.content)
		#
		# for ima in images:
		# 	print(ima)

		# 图片下载,存储
		# for a in range(len(images)):
		# 	name = names[a].split('/')[-1].split('.')[0]
		# 	image = images[a]
		# 	# print(name, '=', image)
		# 	re = requests.request('get', image)
		# 	with open('g:/fuli/' + name + '.jpg', 'wb') as f:
		# 		f.write(re.content)
