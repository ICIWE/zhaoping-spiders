# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import ZhaopingItem


class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/080200%252C020000%252C070300%252C070200,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Connection': 'keep-alive'
    }

    # i = 1   # ############
    # 处理搜索页面，提取下一页连接
    def parse(self, response):
        item = ZhaopingItem()
        position_urls = response.xpath("//div[@class='el']/p[1]/span/a/@href").extract()
        for url in position_urls:
            if self._is_allowed_domains(url):
                yield scrapy.Request(url, callback=self.parse_position, headers=self.headers)
            # else:
            #     item['trouble_url'] = url
            #     yield item

        # 提取下一页连接
        next_page = response.xpath('//a[text()="下一页"]/@href').extract()
        
        if len(next_page) != 0:
            # self.i += 1  # ###########
            next_url = next_page[0]
            yield scrapy.Request(next_url, callback=self.parse, headers=self.headers)

    # 解析职位页面，提取字段
    def parse_position(self, response):

        ##
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        ##
        item = ZhaopingItem()
        position = response.xpath("//div[@class='cn']/h1/text()").extract_first()
        salary = response.xpath("//div[@class='cn']/strong/text()").extract_first()
        location = response.xpath("//p[@class='msg ltype']/text()").extract_first()
        job_msg = response.xpath("//div[contains(@class, 'job_msg')]//text()").re('[^\t\r\n]+')
        company = response.xpath("//a[@class='catn']/text()").extract_first()
        com_people = response.xpath("//p[@class='at'][2]/text()").extract()
        com_trade = response.xpath("//p[@class='at'][3]/text()").extract()
        all_positions = response.xpath("//a[@class='i_house']/@href").extract_first()

        if position:
            item['position'] = position.strip()
        if salary:
            item['salary'] = salary.strip()
        if location:
            item['location'] = location.strip()
        if job_msg:
            item['job_msg'] = job_msg
        if company:
            item['company'] = company.strip()
        if com_people:
            item['com_people'] = com_people[0]
        if com_trade:
            item['com_trade'] = com_trade[0]
        if all_positions:
            item['all_positions'] = all_positions

        yield item

    def _is_allowed_domains(self, url):
        # 判断链接是否为正常职位网页
        if re.match('.*?jobs.51job.*', url):
            return url
        else:
            return None