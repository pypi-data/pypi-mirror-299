# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import time
import json
import re
from scrapy.signalmanager import dispatcher
from scrapy import signals

def normalize_key (text):

    if text is None:
        return ''
    
    if text is not None:
        
        normalized_key = text.replace('(p.m.)','').replace('(s)','').strip()

        # Replace spaces with underscores
        normalized_key = normalized_key.replace(' ', '_').replace('.','').replace('-','_').strip()
    
        # Remove special characters
        normalized_key = ''.join(char for char in normalized_key if char.isalnum() or char in ['_', '-'])

        normalized_key = normalized_key.replace('__',"_")

        # Decapitalize the key
        normalized_key = normalized_key.lower()

        return normalized_key

class RawDataPipeline:

    def __init__(self):
        self.raw_data = []

    def process_item(self, item, spider):
        # Basic data validation: Check if the scraped item is not empty
        adapter = ItemAdapter(item)
        if adapter.get('source'):
            self.raw_data.append(adapter.asdict())
        return item

    def close_spider(self,spider):

        #Process data
        spider.log("pipeline Closing spider and sending custom_closed_signal...")
        dispatcher.send(signal=signals.spider_closed, 
                        sender=spider, 
                        raw_data = self.raw_data)
