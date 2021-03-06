# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo


class TutorialPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing text')


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, port, username, password):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.port = port
        self.username = username
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            port=crawler.settings.get('PORT'),
            username=crawler.settings.get('USERNAME'),
            password=crawler.settings.get('PASSWORD')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri, self.port)
        self.db_auth = self.client.admin
        self.db_auth.authenticate(self.username, self.password)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
