# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanPipeline(object):
    def open_spider(self, spider):
        import xlwt
        workbook = xlwt.Workbook()
        label = ['文学', '流行', '文化', '生活', '经管', '科技']
        for sub_label in label:
            worksheet = workbook.add_sheet(sub_label)
        workbook.save('book_info.xls')
    def process_item(self, item, spider):
        return item
    def close_spider(self, spider):
        pass


