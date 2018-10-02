# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhaopingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    position = scrapy.Field()       # 职位 str
    salary = scrapy.Field()         # 薪资 str
    location = scrapy.Field()       # 工作地点 str
    job_msg = scrapy.Field()        # 职位信息  list
    company = scrapy.Field()        # 公司 str
    com_people = scrapy.Field()     # 公司人数 str
    com_trade = scrapy.Field()      # 行业 str
    all_positions = scrapy.Field()  # 公司所有职位 str
    # trouble_url = scrapy.Field()    # 有问题的链接