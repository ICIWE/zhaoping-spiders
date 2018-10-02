# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class ZhaopingPipeline(object):

    # trouble_urls = []
    con = None 
    cur = None
    def open_spider(self, spider):
        db_name = spider.settings.get('SQLITE_DB_NAME', 'a51job.db')
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        sql = '''
            create table position_info(
                id integer primary key not null,
                position char,
                salary char(10),
                location char(10),
                job_msg text,
                company char(10),
                com_people char(10),
                com_trade char(10),
                all_positions  char)
            '''
        self.cur.execute(sql)

    def close_spider(self, spider):
        self.con.commit()
        self.con.close()

        # for url in self.trouble_urls:
        #     with open('trouble_urls.txt', 'a') as f:
        #         f.write(str(url))

    # def save_trouble_urls(self, item):
    #     if item['trouble_url']:
    #         self.trouble_urls.append(item['trouble_url'])

    def process_item(self, item, spider):

        '''还需清洗数据'''

        # self.save_trouble_urls(item)
        values = (
            item.get('position', 'NULL'),
            item.get('salary', 'NULL'),
            item.get('location','NULL'),
            str(item.get('job_msg', 'NULL')),
            item.get('company', 'NULL'),
            item.get('com_people', 'NULL'),
            item.get('com_trade', 'NULL'),
            item.get('all_positions', 'NULL')
            )
        sql = "insert into position_info(position,salary,location,job_msg,company,com_people,com_trade,all_positions) values(?,?,?,?,?,?,?,?)"
        self.cur.execute(sql, values)
        return item
 