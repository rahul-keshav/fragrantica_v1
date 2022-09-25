import scrapy
import logging
import pandas as pd
import time
df = pd.read_csv("link1.csv")

urls = list(df['URL'])

class BuildSpider(scrapy.Spider):
    name = 'build'
    
    def start_requests(self):
        for url in urls:
            url_with_proxy = 'http://api.scraperapi.com/?api_key=14dd819a8cf83d7d83b364747358f901&url=' + url
            yield scrapy.Request(url=url_with_proxy, callback=self.parse, meta={"original_url":url})
                
            

    def parse(self, response):
        original_url = response.meta["original_url"]
        url =  response.url
        text = response.xpath('//h1/text()').get()        
        gender = response.xpath('//h1/small/text()').get()      
        brand = response.xpath('//span[@class="vote-button-name"]/text()').get()
        accords = response.xpath('//div[@class="cell accord-box"]//text()').getall()
        ac = ','.join(accords)
        perfumers = response.xpath('//div[@class="cell"]/a/text()').getall()
        perfumer = ','.join(perfumers)
        top_notes = response.xpath('//*[@id="pyramid"]/div[1]/div/pyramid-switch/pyramid-level[1]/div/div//text()').getall()
        t_n =','.join(top_notes)
        middle = response.xpath('//*[@id="pyramid"]/div[1]/div/pyramid-switch/pyramid-level[2]/div/div//text()').getall()
        m_n =','.join(middle)
        base = response.xpath('//*[@id="pyramid"]/div[1]/div/pyramid-switch/pyramid-level[3]/div/div//text()').getall()
        b_n =','.join(base)
        
        description_ = response.xpath('//div[@itemprop="description"]/p[1]//text()').getall()
        description = ' '.join(description_)
        long_description_ = response.xpath('//div[@class="fragrantica-blockquote"]//text()').getall()
        long_description = ' '.join(long_description_)
        rating = response.xpath('//span[@itemprop="ratingValue"]/text()').get()
        out_of = response.xpath('//span[@itemprop="bestRating"]/text()').get()
        No_of_vote = response.xpath('//span[@itemprop="ratingCount"]/text()').get()
        No_of_review = response.xpath('//meta[@itemprop="reviewCount"]/@content').get()
        yield{
            'original_url':original_url,
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
            'Base notes':b_n,
            'Rating':rating,
            'Out of ':out_of,
            'Total no of votes':No_of_vote,
            'No_of_review':No_of_review
            # 'user_agent': response.request.headers.get('User-Agent').decode('utf-8')
        }

