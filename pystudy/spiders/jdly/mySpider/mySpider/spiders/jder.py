# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import os

class JderSpider(scrapy.Spider):
    name = 'jder'
    allowed_domains = ['www.jder.net']
    start_urls = ['http://www.jder.net/?s=%E9%AD%94%E7%8E%8B&cat=0']

    def parse(self, response):
        content=response.body
        soup=BeautifulSoup(content,"html.parser")
        a_list=soup.find_all('a', attrs={'href':True,'rel':'bookmark'})
        b_list=a_list[::2]
        for item in b_list:
            post_url=item['href']
            post_id=item['href'].split('/')[4].split('.')[0]
            print(post_url)
            yield Request(url=post_url,callback=self.parse_post_page,meta={'post_id':post_id})

    def parse_post_page(self,response):
        content=response.body
        soup=BeautifulSoup(content,"html.parser")
        temp_title_list=soup.find_all('h1')
        post_id=response.meta['post_id']
        post_url=response.url
        post_title=""
        if len(temp_title_list) !=0:
            post_title=temp_title_list[0].text
        print(post_title+"URL:"+response.url)
        img_list1=soup.find(class_="single-content")
        img_list=img_list1.find_all('img')
        for item in img_list:
            img_url=item['src']
            yield Request(url=img_url,callback=self.down_load_image,
                          meta={'post_id':post_id,'post_title':post_title,'index':img_list.index(item)},
                          dont_filter=True)

    def down_load_image(self,response):
        content=response.body
        index=response.meta['index']
        post_id=response.meta['post_id']
        post_title=response.meta['post_title']
        pic_format=response.url.split('.')[-1]
        #
        file_dir=self.local_file_root+post_title+"/"
        filename=file_dir+str(index)+"."+pic_format
        exist=os.path.exists(file_dir)
        if not exist:
            os.makeirs(file_dir)
        with open(filename,'xb') as file:
            file.write(content)

