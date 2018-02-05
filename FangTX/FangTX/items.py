# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangtxItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 小区名称
    location = scrapy.Field()  # 小区位置
    year = scrapy.Field()  # 小区年代
    mode = scrapy.Field()  # 小区类型

    house_type = scrapy.Field()  # 房型
    area = scrapy.Field()  # 面积
    toward = scrapy.Field()  # 朝向
    floor = scrapy.Field()  # 楼层

    level = scrapy.Field()  # 装修程度
    price = scrapy.Field()  # 房屋单价
    first_pay = scrapy.Field()  # 参考首付
    month_pay = scrapy.Field()  # 参考月付

    total_price = scrapy.Field()  # 房屋总价
    company = scrapy.Field()  # 中介公司
    person = scrapy.Field()  # 中介经理人
    phone = scrapy.Field()  # 经理人手机

    url = scrapy.Field()   # 对应的url
