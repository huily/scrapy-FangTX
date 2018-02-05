# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import time
import datetime

class FangtxPipeline(object):



    #爬虫运行过程中执行的方法
    def process_item(self, item, spider):

        try:

            #将数据写入csv文件
            self.writer.writerow(item)
            print('写入成功')
            pass
        except Exception as e:
            print(Exception, e)
            pass

        return item

    # 重写方法
    def open_spider(self, spider):
        # 序列化csv文件头，即第一行
        self.header = ['name', 'area', 'house_type', 'total_price', 'price', 'location', 'level', 'toward', 'floor', 'year',
                  'company', 'person', 'phone', 'url']
        # 创建/打开文件
        # 获得程序运行时的日期
        date = time.strftime("%Y-%m-%d", time.localtime())
        # 文件名称格式data+运行日期
        file_dir_name = './sources/data-' + date + '.csv'
        self.csvfile = open(file_dir_name, 'w', newline='', encoding='utf-8')   # 以写入模式打开，如果文件存在，覆盖数据

        # csv模块写入数据到csv文件，文件第一行以self.header一致
        self.writer = csv.DictWriter(self.csvfile, self.header)
        # 写入头部，即设置列名
        self.writer.writeheader()

        print('open file ok')
        # 开始时间
        self.start_time = datetime.datetime.now()
        print("启动时间： ", str(self.start_time))

        pass

    # 重写方法
    def close_spider(self, spider):
        # 文件保存数据
        self.csvfile.close()
        print('close file ok')
        # 结束时间
        self.end_time = datetime.datetime.now()
        print("结束时间：", str(self.end_time))
        print('总用时间（min）： ', (self.start_time - self.end_time).seconds/60)
        pass