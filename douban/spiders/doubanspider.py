# !usr/bin/env python
# -*- coding:utf-8 -*-
import scrapy


class DouBan(scrapy.Spider):
    name = "doubanspider"
    def start_requests(self):
        urls=[
            'https://book.douban.com'
        ]
        for url in urls:
            yield scrapy.Request(url,callback=self.parse)
    def parse(self, response):
        pass

    def get_books_hot_label(self,response):
        from bs4 import BeautifulSoup
        label = {}
        #/html/body/div[3]/div[2]/div/div[2]/ul/li[1]
        # hot label:/html/body/div[3]/div[2]/div/div[2]/ul
        '''
        /html/body/div[3]/div[2]/div/div[2]/ul/li[1]/ul/li[1]
        '''
        for total_label in response.xpath('/html/body/div[3]/div[2]/div/div[2]/ul//'):
            for


if __name__ == '__main__':
    pass