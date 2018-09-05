# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest


class WeatherSpider(scrapy.Spider):
    name = "weather"
    header = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    }

    def start_requests(self):
        return [Request('http://218.91.209.251:8087/Account/Login.aspx?ReturnUrl=/Default.aspx',
                        meta={'cookiejar': 1}, callback=self.parse)]

    def parse(self, response):
        data = {
            'ToolkitScriptManager1_HiddenField': ';;AjaxControlToolkit, Version=4.1.60919.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:zh-CN:ee051b62-9cd6-49a5-87bb-93c07bc43d63:de1feab2:f9cec9bc:35576c48',
            '__EVENTTARGET': 'Login1$btnLogin',
            '__VIEWSTATE': '/wEPDwUJLTE2ODA4NjE1ZGS5RDA5RnZQWToByx24bF3EeP4ZcFS5KnWABqJ8ZFt2hw==',
            '__VIEWSTATEGENERATOR': 'CD85D8D2',
            '__EVENTVALIDATION': '/wEWBgKo1vixAQKUvNa1DwL666vYDAL8iti3CgLi6Pi8DgLH/67fCQcJN5rdVcpYg8U3PlWqAF3Bg/dvVdoGZ+VZaZwP5sL3',
            'Login1$UserName': 'yb',
            'Login1$Password': 'yb1',
            'submit': ''
        }

        # 响应Cookie
        cookie1 = response.headers.getlist('Set-Cookie')  # 查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
        print(cookie1)
        print('登录中')
        """第二次用表单post请求，携带Cookie、浏览器代理、用户登录信息，进行登录给Cookie授权"""
        return [FormRequest.from_response(response,
                                          url='http://218.91.209.251:8087/Account/Login.aspx?ReturnUrl=/Default.aspx',
                                          # 真实post地址
                                          meta={'cookiejar': response.meta['cookiejar']},
                                          headers=self.header,
                                          formdata=data,
                                          callback=self.next,
                                          )]

    def next(self, response):
        print('测试,位置===========' + str(response.headers))
        """登录后请求需要登录才能查看的页面，如个人中心，携带授权后的Cookie请求"""
        yield Request('http://218.91.209.251:8087/default.aspx', meta={'cookiejar': True}, callback=self.parse_page)

    def parse_page(self, response):
        print('测试,位置111===========' + str(response))
        # 请求Cookie
        cookie2 = response.request.headers.getlist('Cookie')
        print('cookie2===' + str(cookie2))

        body = response.body  # 获取网页内容字节类型
        unicode_body = response.body_as_unicode()  # 获取网站内容字符串类型
        # with open('db.txt', 'w') as file:
        #     file.write(unicode_body)

        # table = response.xpath('//*[@class="header"]/th[1]//text()').extract()[0]
        # with open('table.txt', 'w') as file:
        #     file.write(table)

        table = response.xpath('//*[@class="gridview"]/tr')
        print(len(table))  # 47
        for x in range(2, len(table) + 1):
            x = str(x)
            # 解析文本
            id = response.xpath('//*[@class="gridview"]/tr[' + x + ']/td[1]/text()').extract()[0]
            so2_ug = response.xpath('//*[@class="gridview"]/tr[' + x + ']/td[2]/text()').extract()[0]
            so2_iaqi = response.xpath('//*[@class="gridview"]/tr[' + x + ']/td[3]/text()').extract()[0]

            # 存储
            dic = {'id': id, 'so2_ug': so2_ug, 'so2_iaqi': so2_iaqi}
            with open('table.txt', 'a', encoding='utf8') as file:
                file.write(str(dic))
                file.write('\n')

