# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class ReviewsPipeline(object):

    collection_name = 'review'
    reviews = []
    
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://root:root@mongo:27017/admin')
        print(f"Connected")
        self.db = self.client.booking
        super().__init__()
    
    def open_spider(self,spider):
        pass

    def close_spider(self, spider):
        
        if self.reviews:
            self.save()
        self.client.close()
    

    def process_item(self, item, spider):
        
        self.reviews.append(dict(item))
        if len(self.reviews)>=100:
            self.save()
        return item
    
    def save(self):
        self.db[self.collection_name].insert_many(self.reviews)
        self.reviews.clear()