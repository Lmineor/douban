# !usr/bin/env python
# -*- coding:utf-8 -*-
import scrapy
import time


class DouBan(scrapy.Spider):
    name = "doubanspider"
    def start_requests(self):
        urls=[
            'https://book.douban.com/tag/?view=type&icn=index-sorttags-all',
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
        }
        for url in urls:
            yield scrapy.Request(url,headers=headers,callback=self.parse)
    def parse(self, response):
        return self.get_book_url(response)

    def get_books_hot_label(self,response):
        book = {}
        for total_label in response.xpath('//*[@id="content"]/div/div[1]/div[2]//div'):
            sum_label = total_label.xpath('a/@name').extract()
            sum_label = ''.join(sum_label)
            book_label_list = []
            for tr in total_label.xpath('./table/tbody//tr'):
                for td in tr.xpath('.//td'):
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
            book_label = book.get(sub_label) #book_label 类似于小说，推理等是label下的一个子label
            time.sleep(2)
            for sub_sub_label in book_label:
                for i in range(50):
                    start='?start=%s&type=T'%(str(20*i))
                    aurl = 'https://book.douban.com/tag/'+ parse.quote(sub_sub_label)+start
                    #aurl = 'https://book.douban.com/tag/' + parse.quote(sub_sub_label) #获取书的每页url
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
                #对字符串进行处理
                pata = r'([\\n\\,\']+)'
                patb = '[0-9]+'
                item['comment_num'] = ''.join(re.findall(patb, comment_num))
                item['book_name'] = (re.sub(pata, '', book_name)).strip()
                item['info'] = (re.sub(pata, '', info)).strip()
                try:
                    star = float(star)
                except:
                    pass
                item['star'] = star
                item['intro'] = (re.sub(pata, '', intro)).strip()
                yield item
                #111.200.13.181
                '''
                'book_name': '\n\n    一只特立独行的猪\n\n\n    \n\n  ',
                 'comment_num': ['30035'],
                'info': '\n        \n  \n  王小波 / 北方文艺出版社 / 2006-4 / 18.80元\n\n      ',
                'intro': '这本书里除了文化杂文，还有给其他书写的序言与跋语。这些序言与跋语也表明了我的一些态度。除此之外，还有一些轻松的随笔。不管什么书，我都不希望它太严肃，这一本也... ',
                 'star': 8.8}
                '''


if __name__ == '__main__':
    pass