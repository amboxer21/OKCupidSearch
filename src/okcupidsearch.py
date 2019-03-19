#!/usr/bin/env python

import re
import time

from selenium import webdriver
from optparse import OptionParser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class OkCupidSearch(object):

    def __init__(self,keyword):
        self.keyword = keyword
        self.driver  = webdriver.Firefox()
        self.driver.get("https://www.okcupid.com/login")

    def switch_to_tab(self,tab_number):
        self.driver.switch_to.window(self.driver.window_handles[tab_number])

    def new_tab(self):
        self.driver.execute_script('window.open();')
        self.switch_to_tab(1)

    def close_tab(self):
        self.driver.execute_script('window.close();')
        self.switch_to_tab(0)

    def find_name_by_profile(self,link):
        self.new_tab()
        self.driver.get(link)
        name = self.driver.find_element_by_xpath("//div[@class='userinfo2015-basics-username']").text
        res = re.search(self.keyword, name, re.M | re.I)
        if res is not None:
            print('Found match: '+str(link))
        else:
            self.close_tab()

    def login(self,email,password):
        uname = self.driver.find_element_by_name("username")
        uname.send_keys(email)
        pword = self.driver.find_element_by_name("password")
        pword.send_keys(password,Keys.RETURN)
        time.sleep(5)

    def browse_matches(self):
        self.driver.find_element_by_link_text('Browse Matches').click()

    def scroll_to_bottom(self):
        try:
            iterator = 0
            while iterator < 20:
                iterator += 1
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                try:
                    end = self.driver.find_element_by_xpath("//*[contains(text(), 'everyone we could find')]")
                    if end.text is not None:
                        break
                except NoSuchElementException:
                    pass
        except Exception as exception:
            pass

    def main(self): 
        elems = self.driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            href = elem.get_attribute("href")
            res  = re.search('https://www.okcupid.com/profile.*\?', href, re.I | re.M)
            if res is not None:
                print res.group()   
                self.find_name_by_profile(res.group())

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option('-e', '--email',
        dest='email', default='example@email.com',
        help='This is your OK Cupid login E-mail.')
    parser.add_option('-p', '--password',
        dest='password', default='password',
        help='This is your OK Cupid login password.')
    parser.add_option('-k', '--keyword',
        dest='keyword', default='keyword',
        help='This is the name you would like to search on OK Cupid.')
    (options, args) = parser.parse_args()

    okcupidsearch = OkCupidSearch(options.keyword)
    okcupidsearch.login(options.email,options.password)
    okcupidsearch.browse_matches()
    okcupidsearch.scroll_to_bottom()
    okcupidsearch.main()
