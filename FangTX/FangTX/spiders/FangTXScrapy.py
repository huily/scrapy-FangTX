# -*- coding: utf-8 -*-

import scrapy
import re
from FangTX.items import FangtxItem



class FangTX(scrapy.Spider):
    # 爬虫名字
    name = "fangTX"
    # 爬取范围
    #allowed_domains = ["http://esf.gz.fang.com/house-a080/"]
    # 爬取开始页
    start_urls = ["http://esf.gz.fang.com/house-a080"]


    def parse(self, response):

        # 初始化item
        item = FangtxItem()
        # 接收response对象
        resp = scrapy.Selector(response)
        # 提取页面中房屋信息列表, 内容是随机出的
        houseList = resp.css(".houseList")[0].css("dl")
        # 得到url
        for i in houseList:
            dt_a = i.css("dt a")
            # 去除空白，源页面中存在
            if len(dt_a) == 1:
                # 提取url
                url = dt_a.xpath("@href")[0].extract()

                # 爬虫进行二级页面信息提取
                req = scrapy.Request(
                    url = "http://esf.gz.fang.com" + url,
                    meta = {'item':item},
                    callback = self.parse_info,
                    dont_filter = True
                )

                yield req

        # 页面“下一页”
        next_page = resp.css("a#PageControl1_hlk_next").xpath("@href").extract_first()
        # 最后页面是否还有“下一页”
        if next_page is not None:
            next_page_url = "http://esf.gz.fang.com" + next_page
            # 递归调用自身，实现自动下一页爬取url
            yield scrapy.Request(
                url = next_page_url,
                callback = self.parse
            )






    # 爬取详细信息的方法
    def parse_info(self, response):

        # 使用同一个item
        item = response.meta['item']
        # 读取详细信息
        rcont = response.xpath("//div [@class='rcont']/a/text()").extract()
        item['name'] = rcont[0]   # 小区名称
        item['location'] = rcont[2].strip() + " " + rcont[3].strip()   # 小区位置
        text_item = response.xpath("//div [@class='text-item clearfix']//span [@class='rcont']/text()").extract()

        if len(re.findall(r'年', text_item[0])) != 0:
            item['year'] = text_item[0]           # 年代
        else:
            item['year'] = "暂无资料年"  # 年代

        item['total_price'] =  response.css("div.trl-item.price_esf.sty1").xpath("string(i)").extract_first()     # 总价格

        item['url'] = response.url  # url
        item['house_type'] =  response.css("div.tt").xpath("string()").extract()[0].strip()  # 房型
        item['area'] =  re.findall("[0-9]+", response.css("div.tt").xpath("string()").extract()[1].strip())[0] # 面积
        item['price'] = re.findall("[0-9]+", response.css("div.tt").xpath("string()").extract()[2].strip())[0] # 单价
        item['toward'] = response.css("div.tt").xpath("string()").extract()[3].strip()  # 朝向
        item['floor'] = response.css("div.tt").xpath("string()").extract()[4].strip()  # 楼层
        item['level'] = response.css("div.tt").xpath("string()").extract()[5].strip()  # 装修程度

        item['person'] = response.css("span.zf_jjname").xpath("string(a)").extract_first().strip()  # 中介经理人
        item['company'] = response.css("div.tjcont-list-cline2 span")[1].xpath("text()").extract_first()  # 中介公司
        item['phone'] = response.css("div.tjcont-list-cline3 span").xpath("text()").extract_first()  # 中介经理人手机

        # 保存item
        yield item

