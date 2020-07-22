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
import pandas as pd
from tqdm import tqdm



class MediumPost(scrapy.Spider):
    name='medium_scrapper'
    handle_httpstatus_list = [401,400]

    # autothrottle_enabled=True


    # def write_to_file(self):
    #     date_post = self.d.split('/')
    #     year = date_post[0]
    #     month = date_post[1]
    #     day = date_post[2]
    #     # date_post=response.meta['reqDate']
    #     date_post=self.d.replace("/","")
    #     directory=datetime.now().strftime("%Y%m%d")
    #
    #     directory = self.tagSlug
    #     path=directory+"/"+year+"/"+month+"/"
    #     file_name = self.tagSlug+date_post+".json"
    #     if not os.path.exists(path):
    #         os.makedirs(path)
    #
    #     df = pd.DataFrame(self.output_data)
    #     # import pdb; pdb.set_trace()
    #
    #     df.to_json(path+file_name)
    #     print("WRITING TO FILE")

    def start_requests(self):

        start_url = 'https://medium.com/tag/'+self.tagSlug.strip("'")+'/archive/'
        print('start url: ', start_url)

        startDate=datetime.strptime(self.start_date,"%Y%m%d")
        endDate=datetime.strptime(self.end_date,"%Y%m%d")
        delta=endDate-startDate
        print('delta ', delta)

        for i in range(delta.days + 1):
            d=datetime.strftime(startDate+timedelta(days=i),'%Y/%m/%d')
            self.d = d
            self.output_data=[]

            print('start_url+d:', start_url+d)
            yield scrapy.Request(start_url+d,method="GET",callback=self.parse_archive_page)

            # import pdb; pdb.set_trace()
            # self.write_to_file()

    def parse_archive_page(self,response):

        response_data=response.text
        urls = re.findall('data-action-value="(https://medium.com/[@\w.]+/.+?)\?source=tag_archive\-+', response_data)

        urls=list(set(urls))

        for url in urls:
            yield scrapy.Request(url,method="GET",callback=self.parse_article)

    def parse_article(self,response):
        response_data=response.text

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

        parsed_data = {"tags":tags,
                    "title":title,
                    "author":author,
                    "claps":claps,
                    "length":length,
                    "url":url}


        self.output_data.append(parsed_data)
        import pdb; pdb.set_trace()
        yield self.output_data

    # def closed(self, spider):
    #     '''
    #     runs when spider is closed.
    #     export data to json file.
    #     '''
        # date_post = self.d.split('/')
        # year = date_post[0]
        # month = date_post[1]
        # day = date_post[2]
        # # date_post=response.meta['reqDate']
        # date_post=self.d.replace("/","")
        # directory=datetime.now().strftime("%Y%m%d")
        #
        # directory = self.tagSlug
        # path=directory+"/"+year+"/"+month+"/"
        # file_name = self.tagSlug+date_post+".json"
        # if not os.path.exists(path):
        #     os.makedirs(path)
        #
        # df = pd.DataFrame(self.output_data)
        #
        # df.to_json(path+file_name)
        # write_to_file(spider)
