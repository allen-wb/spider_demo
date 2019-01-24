import scrapy
from scrapy.http import Request


class DoubanSpider(scrapy.Spider):
    name = "douban"  # 我们执行文件时的名字
    # 这个列表中的url可以有多个，它会依次都执行，我们这里简单爬取一个
    start_urls = ["https://movie.douban.com/top250"]
    url = "https://movie.douban.com/top250"

    def parse(self, response):  # 默认函数parse
        sites = response.xpath('//ol[@class="grid_view"]')
        # print("！！！！！返回信息是：")
        info = sites.xpath('./li')
        # 从sites中我们再进一步获取到所有电影的所有信息
        for i in info:
            # 排名
            num = i.xpath('./div//em[@class=""]//text()').extract()  # 获取到的为列表类型
            # extract()是提取器  将我们匹配到的东西取出来
            num = '排名:' + num[0] + "; "
            # 标题
            title = i.xpath('.//span[@class="title"]/text()').extract()
            title = "标题: " + title[0] + "; "
            # 评论
            remark = i.xpath('.//span[@class="inq"]//text()').extract()
            remark = "评论: " + ("" if len(remark) < 1 else remark[0]) + "; "
            # 分数
            score = i.xpath('./div//span[@class="rating_num"]//text()').extract()
            score = "评分: " + score[0]
            with open('douban.txt', 'a', encoding='utf8') as f:
                f.write(num + title + remark + score)
                f.write("\r")

        nextlink = response.xpath('//span[@class="next"]/link/@href').extract()
        if nextlink:  # 翻到最后一页是没有连接的，所以这里我们要判断一下
            nextlink = nextlink[0]
            # yield中断返回下一页的连接到parse让它重新从下一页开始爬取，callback返回函数定义返回到哪里
            yield Request(self.url + nextlink, callback=self.parse)
