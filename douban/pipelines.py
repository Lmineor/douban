# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanPipeline(object):
    def open_spider(self, spider):
        from openpyxl import Workbook
        self.wb = Workbook()
        self.sheet =self.wb.active
        self.sheet.title = "豆瓣图书"
        self.label = ['文学', '流行', '文化', '生活', '经管', '科技']
        self.row = 1
        self.sheet["A%d" % (self.row)].value ='序号'
        self.sheet["B%d" % (self.row)].value = '书名'
        self.sheet["C%d" % (self.row)].value = '评论数'
        self.sheet["D%d" % (self.row)].value = '作者及出版社信息'
        self.sheet["E%d" % (self.row)].value = '评价'
        self.sheet["F%d" % (self.row)].value = '简介'


    def process_item(self, item, spider):
        '''
        write itme into excel
        :param item:
        :param spider:
        :return:
        '''
        self.row +=1
        self.sheet["A%d" % (self.row)].value = self.row #为excel添加序号列
        self.sheet["B%d" % (self.row)].value = item['book_name']
        self.sheet["C%d" % (self.row)].value = item['comment_num']
        self.sheet["D%d" % (self.row)].value = item['info']
        self.sheet["E%d" % (self.row)].value = item['star']
        self.sheet["F%d" % (self.row)].value = item['intro']
        self.wb.save('book_info.xlsx')
        return item
    def close_spider(self, spider):
        self.wb.save('book_info.xlsx')


