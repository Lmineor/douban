# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanPipeline(object):
    def open_spider(self, spider):
        import xlwt
        self.workbook = xlwt.Workbook()
        self.label = ['文学', '流行', '文化', '生活', '经管', '科技']
        self.worksheet = self.workbook.add_sheet('豆瓣图书')
        self.row = 0
        self.col = 0
        self.worksheet.write(self.row, self.col, '序号')
        self.col += 1
        self.worksheet.write(self.row, self.col,'书名')
        self.col += 1
        self.worksheet.write(self.row, self.col, '作者及出版社信息')
        self.col += 1
        self.worksheet.write(self.row, self.col, '评论数')
        self.col += 1
        self.worksheet.write(self.row, self.col, '简介')
        self.col += 1


    def process_item(self, item, spider):
        '''
        write itme into excel
        :param item:
        :param spider:
        :return:
        '''
        self.row +=1
        self.worksheet.write(self.row, self.col, self.row)
        self.col += 1
        self.worksheet.write(self.row,self.col,item['book_name'])
        self.col +=1
        self.worksheet.write(self.row,self.col, item['comment_num'])
        self.col +=1
        self.worksheet.write(self.row,self.col, item['info'] )
        self.col +=1
        self.worksheet.write(self.row,self.col, item['star'])
        self.col +=1
        self.worksheet.write(self.row,self.col, item['intro'])
        self.row +=1
        self.col = 0
        return item
    def close_spider(self, spider):
        self.workbook.save('book_info.xls')


