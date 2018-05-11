# !usr/bin/env python
# -*- coding:utf-8 -*-
import scrapy


class DouBan(scrapy.Spider):
    name = "doubanspider"
    def start_requests(self):
        urls=[
            'https://book.douban.com/tag/?view=type&icn=index-sorttags-hot#%E6%96%87%E5%AD%A6'
        ]
        for url in urls:
            yield scrapy.Request(url,callback=self.get_books_hot_label)
    def parse(self, response):
        pass

    def get_books_hot_label(self,response):
        from bs4 import BeautifulSoup
        label = {}
        #/html/body/div[3]/div[2]/div/div[2]/ul/li[1]
        # hot label:/html/body/div[3]/div[2]/div/div[2]/ul
        '''
        /html/body/div[3]/div[2]/div/div[2]/ul/li[1]/ul/li[1]
        /html/body/div[3]/div[1]/div/div[1]/div[2]
        /html/body/div[3]/div[1]/div/div[1]/div[2]/div[1]/table/tbody
        /html/body/div[3]/div[1]/div/div[1]/div[2]/div[1]/table/tbody
        
        '''
        print('s')
        for total_label in response.xpath('//*[@id="content"]/div[1]/div/div[1]/div[2]//'):
            for tr in total_label.xpath('/div[1]/table/tbody//'):
                for td in tr.xpath('/tr[1]/td//'):
                    book_label = td.xpath('a/text()').extract()
                    print('a')
                    print(book_label)


if __name__ == '__main__':
    pass