from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,random,string,os

def rs(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

driver = webdriver.Firefox()
driver.get("http://10.0.2.15:8222")

u,p = rs(10),rs(10)
driver.find_element_by_id("Register_ref").click()
driver.find_element_by_id("usr").send_keys(u)
driver.find_element_by_id("pwd").send_keys(p)
driver.find_element_by_id("submit_login").click()
driver.find_element_by_id("Login_ref").click()
driver.find_element_by_id("submit_login").click()
driver.find_element_by_id("userfile").send_keys(os.getcwd()+"/../input.mp4")
driver.find_element_by_id("userstart").send_keys('5')
driver.find_element_by_id("userdur").send_keys('10')
driver.find_element_by_id("sendfile").click()


time.sleep(30)
driver.close()
