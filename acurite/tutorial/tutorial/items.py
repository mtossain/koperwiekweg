# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
   name = "tutorial"
    
    allowed_domains = ["www.myacurite.com"]
    
    start_urls = [
        "https://www.myacurite.com/#/login",
        "https://www.myacurite.com/#/dashboard"
         ]

    def parse(self, response):
	    return scrapy.FormRequest.from_response(
		    response,
		    formdata={'ctl00$ContentPlaceHolder1$Logincontrol1$txtUserName': 'h.j.van.veluw@gmail.nl', 'ctl00$ContentPlaceHolder1$Logincontrol1$txtPassword': Password,  'ctl00$ContentPlaceHolder1$Logincontrol1$LoginBtn': ''},
		    callback=self.after_login
		)
	   
    def after_login(self, response):
        # check login succeed before going on
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)
