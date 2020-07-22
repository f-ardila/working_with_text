# -*- coding: utf-8 -*-
"""
based off https://github.com/AiswaryaSrinivas/Scraping-Medium-and-Data-Analysis/blob/master/medium_scrapper_tag_archive.py
This scrapper extracts data for a given date range for a particular Medium Tag

to run:
`scrapy runspider -a tagSlug='tagSlug' -a start_date=YYYYmmdd -a end_date=YYYYmmdd medium_scrapper_tag_archive.py`
e.g. `scrapy runspider -a tagSlug='wellness' -a start_date=20200101 -a end_date=20200601 medium_scrapper_tag_archive.py`
"""

import scrapy
from datetime import datetime
from datetime import timedelta
import os
import re
from scrapy.exporters import JsonItemExporter
# from scrapy.utils.log import configure_logging



class MediumPost(scrapy.Spider):
    name='medium_scrapper'
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }
    total_articles = 0
    def start_requests(self):

        startDate=datetime.strptime(self.start_date,"%Y%m%d")
        endDate=datetime.strptime(self.end_date,"%Y%m%d")
        delta=endDate-startDate

        base_url = start_url = 'https://medium.com/tag/'+self.tag+'/archive/'
        self.start_urls=[base_url+datetime.strftime(startDate+timedelta(days=i),'%Y/%m/%d') for i in range(delta.days + 1)]
        print(self.start_urls)
        for start_url in self.start_urls:


            yield scrapy.Request(start_url)


    def parse(self,response):

        response_data=response.text
        # import pdb; pdb.set_trace()


        if response._url in self.start_urls:
            # self.date = response._url[-10:].replace('/','')
            article_urls = re.findall('data-action-value="(https://medium.com/[@\w.]+/.+?)\?source=tag_archive\-+', response_data)
            article_urls=list(set(article_urls))
            date = response._url[-10:].replace('/','')

            self.total_articles +=len(article_urls)
            print('***** {0} articles on {1}, {2} total articles so far ****'.format(len(article_urls), date,self.total_articles))

            for url in article_urls:
                yield scrapy.Request(url,callback=self.parse)

        else:
            date = re.findall('"datePublished":"([0-9-]+)T', response_data)[0]
            try:
                tags= set(re.findall('"Tag:([a-z-]+)"', response_data))
            except:
                tags = re.findall('href="/tag/([\w-]+?)"', response_data)

            css_title = response.css('title::text').getall()[0].split(' | ')
            try:
                #doesn't work for all, but when it does it works better than css_title[0]
                title = re.findall('"og:title" content="([\w .:,?!-/“]+)"', response_data)[0]
            except:
                title = css_title[0]
            try:
                author = re.findall('name="author" content="([\w .:,-]+)"', response_data)[0]
            except:
                author = css_title[1][3:] #remove "by "

            claps = int(re.findall('"clapCount":([0-9]+)', response_data)[0])
            length = int(re.findall('value="([0-9]+) min read"', response_data)[0])
            url = response._url
            comments = None
            author_bio = None
            subtitle = None

            parsed_data = {"date":date,
                        "tags":tags,
                        "title":title,
                        "author":author,
                        "claps":claps,
                        "length":length,
                        "url":url}



            yield parsed_data
