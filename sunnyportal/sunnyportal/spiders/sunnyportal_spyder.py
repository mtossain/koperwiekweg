import scrapy

Password = open('/home/pi/AuthSunnyportalWebsite.txt','r').read().split('\n')[0]
	
class DmozSpider(scrapy.Spider):
    
    name = "sunnyportal"
    allowed_domains = ["www.sunnyportal.com"]
    start_urls = [
        "https://www.sunnyportal.com/Templates/Start.aspx?ReturnUrl=%2fTemplates%2fNoticePage.aspx",
        "https://www.sunnyportal.com/FixedPages/HoManLive.aspx",
		"https://www.sunnyportal.com/FixedPages/Dashboard.aspx"
         ]

    def parse(self, response):
	    return scrapy.FormRequest.from_response(
		    response,
		    formdata={'ctl00$ContentPlaceHolder1$Logincontrol1$txtUserName': 'h.j.van.veluw@hccnet.nl', 'ctl00$ContentPlaceHolder1$Logincontrol1$txtPassword': Password,  'ctl00$ContentPlaceHolder1$Logincontrol1$LoginBtn': ''},
		    callback=self.after_login
		)
	   
    def after_login(self, response):
        # check login succeed before going on
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)		
