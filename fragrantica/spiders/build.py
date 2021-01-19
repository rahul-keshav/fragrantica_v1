import scrapy
import logging
import pandas as pd
import time
import csv
from shutil import which
df = pd.read_csv("fragrantica/spiders/link.csv")

ls = list(df['URL'])

class BuildSpider(scrapy.Spider):
    name = 'build'
    
    def start_requests(self):
        i = int(input('enter the start index,index start from 1:  '))
        j = int(input('enter the last index:  '))        
        urls = ls[i-1:j]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        url =  response.url
        text = response.xpath('//*[@id="toptop"]/h1/text()').get()        
        gender = response.xpath('//*[@id="toptop"]/h1/small/text()').get()      
        brand = response.xpath('//*[@id="main-content"]/div[1]/div[1]/div/div[2]/div[1]/div[2]/p/a/span/text()').get()
        accords = response.xpath('//*[@id="main-content"]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div//text()').getall()
        ac = ','.join(accords)
        perfumers = response.xpath('////div[@class="cell"]/a/text()').getall()
        perfumer = ','.join(perfumers)
        top_notes = response.xpath('//*[@id="pyramid"]/div[1]/div/pyramid-switch/pyramid-level[1]/div/div//text()').getall()
        t_n =','.join(top_notes)
        middle = response.xpath('//*[@id="pyramid"]/div[1]/div/pyramid-switch/pyramid-level[2]/div/div//text()').getall()
        m_n =','.join(middle)
        description_ = response.xpath('//*[@id="main-content"]/div[1]/div[1]/div/div[2]/div[5]/div/p[1]//text()').getall()
        description = ' '.join(description_)
        long_description_ = response.xpath('//div[@class="fragrantica-blockquote"]//text()').getall()
        long_description = ' '.join(long_description_)
        rating = response.xpath('//*[@id="main-content"]/div[1]/div[1]/div/div[2]/div[4]/div[3]/div/p/span[1]/text()').get()
        out_of = response.xpath('//*[@id="main-content"]/div[1]/div[1]/div/div[2]/div[4]/div[3]/div/p/span[2]/text()').get()
        No_of_vote = response.xpath('//*[@id="main-content"]/div[1]/div[1]/div/div[2]/div[4]/div[3]/div/p/span[3]/text()').get()
        yield{
            'Url':url,
            'Title':text,
            'Brand':brand,
            'Gender':gender,
            'Accords':ac,
            'Short Description':description,
            'long Description':long_description,
            'Perfumer':perfumer,
            'Top notes':t_n,
            'Middle notes':m_n,
            'Rating':rating,
            'Out of ':out_of,
            'Total no of votes':No_of_vote,
            # 'user_agent': response.request.headers.get('User-Agent').decode('utf-8')
        }

