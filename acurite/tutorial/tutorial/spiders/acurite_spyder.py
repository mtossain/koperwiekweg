# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#class DmozSpider(scrapy.Spider):
    #name = "dmoz"
    #allowed_domains = ["dmoz.org"]
    #start_urls = [
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    #]

    #def parse(self, response):
        #filename = response.url.split("/")[-2]
        #with open(filename, 'wb') as f:
            #f.write(response.body)
            
from loginform import fill_login_form

class TutorialItem(scrapy.Spider):
    # define the fields for your item here like:
    name = "acurite"
    Password = 'Snoetje01#'
    
    allowed_domains = ["www.myacurite.com"]
    
    start_urls = ['https://www.myacurite.com']
    
    login_url = 'https://www.myacurite.com'
    login_user = 'h.j.van.veluw@gmail.com' 
    login_password = 'Snoetje01#'



    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'method':'post' ,'email': 'h.j.van.veluw@gmail.com', 'password': 'Snoetje01#','submit':''},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return
            
    #def start_requests(self):
        ## let's start by sending a first request to login page
        #yield scrapy.Request(self.login_url, self.parse_login)
    
    #def parse_login(self, response):
        ## got the login page, let's fill the login form...
        #data, url, method = fill_login_form(response.url, response.body,
                                            #self.login_user, self.login_password)

        ## ... and send a request with our login data
        #return FormRequest(url, formdata=dict(data),
                           #method=method, callback=self.start_crawl)

    #def start_crawl(self, response):
        ## OK, we're in, let's start crawling the protected pages
        #for url in self.start_urls:
            #yield scrapy.Request(url)
            

    #def after_login(self, response):
        # check login succeed before going on
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)
