# !usr/bin/env python
# -*- coding:utf-8 -*-
import scrapy
import time


class DouBan(scrapy.Spider):
    name = "doubanspider"
    def start_requests(self):
        urls=[
            'https://book.douban.com/tag/?view=type&icn=index-sorttags-hot#%E6%96%87%E5%AD%A6',
        ]
        for url in urls:
            yield scrapy.Request(url,callback=self.parse)
    def parse(self, response):
        return self.get_book_url(response)

    def get_books_hot_label(self,response):
        book = {}
        for total_label in response.xpath('//*[@id="content"]/div/div[1]/div[2]//div'):
            sum_label = total_label.xpath('a/@name').extract()
            sum_label = ''.join(sum_label)
            book_label_list = []
            time.sleep(1)
            for tr in total_label.xpath('./table/tbody//tr'):
                for td in tr.xpath('.//td'):
                    time.sleep(1)
                    book_label = td.xpath('a/text()').extract()
                    book_label = ''.join(book_label)
                    book_label_list.append(book_label)
            book[sum_label] = book_label_list
        return book

    def get_book_url(self,response):
        '''
        获取每一类型的书的标签
        :param response:
        :return:
        '''
        from urllib import parse
        import time
        book = self.get_books_hot_label(response)
        label = ['文学', '流行', '文化', '生活', '经管', '科技']
        book_url = []
        for sub_label in label:
            book_label = book.get(sub_label)
            time.sleep(1)
            for sub_sub_label in book_label:
                aurl = 'https://book.douban.com/tag/' + parse.quote(sub_sub_label)
                time.sleep(1)
                yield scrapy.Request(aurl,callback=self.parse_page)
                book_url.append(aurl)

    def parse_page(self,response):
        '''
        对每一个标签页中的内容进行提取
        :param response:
        :return:
        '''
        import re
        from douban.items import DoubanItem
        item = DoubanItem()
        #//*[@id="subject_list"]/ul
        for subject_itme in response.xpath('//*[@id="subject_list"]/ul//li'):
            for bookinfo in subject_itme.xpath('./div[2]'):
                book_name = ''.join(bookinfo.xpath('./h2/a/text()').extract())
                info = ''.join(bookinfo.xpath('./div[1]/text()').extract())
                star= ''.join(bookinfo.xpath('./div[2]/span[2]/text()').extract())
                comment_num = ''.join(bookinfo.xpath('./div[2]/span[3]/text()').extract())
                intro = ''.join(bookinfo.xpath('./p/text()').extract())
                item['book_name'] = book_name
                item['info'] = info
                item['star'] = float(star)
                pat = '[0-9]+'
                item['comment_num'] = re.findall(pat,comment_num)
                print(re.findall(pat,comment_num))
                item['intro'] = intro
                yield item
                #111.200.13.181


if __name__ == '__main__':
    pass