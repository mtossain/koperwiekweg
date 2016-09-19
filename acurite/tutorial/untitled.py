import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://www.myacurite.com")
time.sleep(4)

#driver.switch_to_frame('main')
textinput = driver.find_element_by_name('email')
textinput.send_keys("h.j.van.veluw@gmail.com")
textinput = driver.find_element_by_name('password')
textinput.send_keys("Snoetje01#")
time.sleep(1)
button = driver.find_element_by_xpath('//input[@value="Log In"]')
button.click()
driver.close()
