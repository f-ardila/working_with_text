# -*- coding: utf-8 -*-
"""
based off https://github.com/AiswaryaSrinivas/Scraping-Medium-and-Data-Analysis/blob/master/medium_scrapper_tag_archive.py
This scrapper extracts data for a given date range for a particular Medium Tag

to run:
`scrapy runspider medium_tag_crawler.py`
e.g. `scrapy runspider medium_tag_crawler.py`
"""

import scrapy
from scrapy.exceptions import CloseSpider
import os
import re



class MediumPost(scrapy.Spider):
    name='medium_tag_scrapper'
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1
    }
    total_tags = 0
    # tags={'name':'wellness', 'postCount':0, 'related_tags':[]}
    tags={}
    starting_tag = 'wellness'
    postCount_limit = 1e5

    def start_requests(self):

        # startDate=datetime.strptime(self.start_date,"%Y%m%d")
        # endDate=datetime.strptime(self.end_date,"%Y%m%d")
        # delta=endDate-startDate

        self.base_url = 'https://medium.com/tag/'
        self.start_url= self.base_url + self.starting_tag
        print(self.start_url)

        yield scrapy.Request(self.start_url)


    def parse(self,response):

        response_data = response.text

        #for literal parsing with eval()
        true = True
        false = False

        parentTag_data = eval(re.findall('"tag":({.+?,"type":"Tag"}),',response_data)[-1])
        parentTag = parentTag_data['slug']
        parentTag_postCount = parentTag_data['postCount']
        relatedTags_list = re.findall('"relatedTags":(\[{.+,"type":"Tag"}])}\)',response_data)

        if relatedTags_list == []:
            relatedTag_names = []
        else:
            relatedTags = eval(relatedTags_list[-1])
            relatedTag_dic = {tag['slug']:tag['postCount'] for tag in relatedTags}
            # relatedTag_counts = [tag['postCount'] for tag in relatedTags]


        self.tags[parentTag] = {'name':parentTag,'postCount' : parentTag_postCount,'relatedTags': relatedTag_dic}

        # try:
            # relatedTags_string = re.findall('"relatedTags":(\[[\w\{\}\"\'‘’:;,-.*@“”\(\)/|+&%!#$<>~—\u200a ]+\])',response_data)[-1]

        for tag, postCount in relatedTag_dic.items():
            # import pdb; pdb.set_trace()
            if tag not in self.tags and postCount >= self.postCount_limit:
                print(tag)

                postCount >= self.postCount_limit

                yield scrapy.Request(self.base_url + tag)


            else:
                pass
        # except IndexError:
        #     if re.findall('"relatedTags":\[{"slug"',response_data) == []:
        #         self.tags[parentTag]['relatedTags'] = []
        #     else:
        #         import pdb; pdb.set_trace()
        yield self.tags[parentTag]
        # if len(self.tags)>10:
        #     # yield self.tags
        #     raise CloseSpider('over 1000 tags')



    def closed(self, spider):
        print('{0} tags'.format(len(self.tags)))
        print(self.tags)



        # if response._url in self.start_urls:
        #     # self.date = response._url[-10:].replace('/','')
        #     article_urls = re.findall('data-action-value="(https://medium.com/[@\w.]+/.+?)\?source=tag_archive\-+', response_data)
        #     article_urls=list(set(article_urls))
        #     date = response._url[-10:].replace('/','')
        #
        #     self.total_articles +=len(article_urls)
        #     print('***** {0} articles on {1}, {2} total articles so far ****'.format(len(article_urls), date,self.total_articles))
        #
        #     for url in article_urls:
        #         yield scrapy.Request(url,callback=self.parse)
        #
        # else:
        #     date = re.findall('"datePublished":"([0-9-]+)T', response_data)[0]
        #     try:
        #         tags= set(re.findall('"Tag:([a-z-]+)"', response_data))
        #     except:
        #         tags = re.findall('href="/tag/([\w-]+?)"', response_data)
        #
        #     css_title = response.css('title::text').getall()[0].split(' | ')
        #     try:
        #         #doesn't work for all, but when it does it works better than css_title[0]
        #         title = re.findall('"og:title" content="([\w .:,?!-/“]+)"', response_data)[0]
        #     except:
        #         title = css_title[0]
        #     try:
        #         author = re.findall('name="author" content="([\w .:,-]+)"', response_data)[0]
        #     except:
        #         author = css_title[1][3:] #remove "by "
        #
        #     claps = int(re.findall('"clapCount":([0-9]+)', response_data)[0])
        #     length = int(re.findall('value="([0-9]+) min read"', response_data)[0])
        #     url = response._url
        #     comments = None
        #     author_bio = None
        #     subtitle = None
        #
        #     parsed_data = {"date":date,
        #                 "tags":tags,
        #                 "title":title,
        #                 "author":author,
        #                 "claps":claps,
        #                 "length":length,
        #                 "url":url}
        #
        #
        #
        #     yield parsed_data
