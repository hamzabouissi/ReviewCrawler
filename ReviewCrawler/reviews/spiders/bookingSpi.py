# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import json
from datetime import datetime
from reviews.items import ReviewsItem
from scrapy.loader import ItemLoader

import pymongo

class BookingspiSpider(scrapy.Spider):
    
    name = 'bookingSpi'
    allowed_domains = ['booking.com']
    payload = "?cc1=sa&pagename={}&rows=25&offset={}"
    review_url  = "https://www.booking.com/reviewlist.en-gb.html"
    base_url = "https://www.booking.com/searchresults.en-gb.html?ss=Makkah%2BAl%2BMukarramah%2BProvince,%2BSaudi%2BArabia&is_ski_area&ss_raw=Mecca&ac_langcode=en&dest_type=region&region_type=province&rows=25&offset={}"
    offset = 0
    
    
    
    def parse(self, response):
        pass

    
    def ReviewFinder(self,response,pagename,offset):

        data = []
        
        html = BeautifulSoup(response.text,'lxml')
        reviews = html.find_all('div',class_='c-review-block')
        next_page = html.find('div',class_='bui-pagination__item bui-pagination__next-arrow')
        for review in reviews:
            poor = ''
            title = review.find('h3',class_='c-review-block__title')
            username = review.find('span',class_='bui-avatar-block__title')
            country = review.find('span',class_='bui-avatar-block__subtitle')
            review_date = review.find('span',class_='c-review-block__date')
            score = review.find('div',class_='bui-review-score__badge')
            comment = review.find_all('span',class_='c-review__body')
            room_info = review.find('div',class_='room_info_heading')
            res_date = review.find('span',class_='c-review-block__date')
            #response = review.find('span',class_='c-review-block__response__body')
            if len(comment)==2:
                poor = comment[1].get_text().strip()
            if room_info:
                room_info = room_info.get_text()
            else:
                room_info = None
            review_date = datetime.strptime(" ".join(review_date.get_text().strip().split(" ")[1:]),"%d %B %Y").strftime("%Y-%m-%d")
            if title and username and country and score and comment :
                yield ReviewsItem(**{
                    'title':title.get_text().strip(),
                    'username':username.get_text().strip(),
                    'country':country.contents[1].strip(),
                    'review_date':review_date,
                    'score':score.get_text(),
                    'room_info':room_info,
                    "good":comment[0].get_text().strip(),
                    "poor":poor,
                    'createdAt':datetime.now()
                    }
                )
                pass
        offset+=25
        if next_page:
            url = "https://booking.com" + next_page.a.attrs['href']
            
            yield scrapy.Request(url,callback=self.ReviewFinder,cb_kwargs=dict(pagename=pagename,offset=offset))

    def start_requests(self):
        
        
        yield scrapy.Request(self.base_url.format(self.offset),callback=self.Hotels)

    def Hotels(self,response):
        
        page = BeautifulSoup(response.text,"lxml")
        for hotel in page.find_all("a",class_="hotel_name_link url"):
            pagename = hotel.attrs['href'].split(".")[0].split("/")[-1]
            url = self.review_url+self.payload.format(pagename,0)
            
            yield scrapy.Request(url,callback=self.ReviewFinder,cb_kwargs=dict(pagename=pagename,offset=0))
        self.offset+=25  
        self.logger.info("New Request")
        yield self.start_requests()
    
    