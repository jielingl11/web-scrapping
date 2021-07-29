# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 20:02:23 2021

@author: user
"""

# import packages 


import urllib
import requests
import re
from selenium import webdriver



# test if the browser can open 

def google_results_open_browser(keyword):
    info_raw_t=[]
    info_raw_l=[]
    
    html_keyword= urllib.parse.quote_plus(keyword)
    url = 'https://www.google.com/search?q=' + html_keyword
    driver = webdriver.Chrome(r'C:\Users\user\Data\webscraping_homepages\webdriver\chromedriver.exe')
    driver.get(url)
    
    for element in driver.find_elements_by_xpath('//div[@class="g"]'):
        title = element.find_element_by_xpath('.//h3').text
        link = element.find_element_by_xpath('.//div[@class="yuRUbf"]/a').get_attribute('href')
        info_raw_l.append(link.lower())     
        info_raw_t.append(title.lower())
        
    return info_raw_l, info_raw_t

# get all title and url of the google results from page one to page n 
# where n is a number you assign 

def google_results(start, end, keyword): 
    info_raw_t=[]
    info_raw_l=[]
    end= end+ 1
    start= start- 1
    for i in range(start, end):
        number= str(10*i)
        html_keyword= urllib.parse.quote_plus(keyword)
        url = 'https://www.google.com/search?q=' + html_keyword+ '&start='+number
        options = webdriver.ChromeOptions()
        PATH= r"C:\Users\user\Data\web-scrapping\webdriver\chromedriver.exe"
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(executable_path = PATH, options=options)
        driver.get(url)
        
        for element in driver.find_elements_by_xpath('//div[@class="g"]'):
            title = element.find_element_by_xpath('.//h3').text
            link = element.find_element_by_xpath('.//div[@class="yuRUbf"]/a').get_attribute('href')
            info_raw_l.append(link.lower())     
            info_raw_t.append(title.lower())
        
    return info_raw_l, info_raw_t



def bing_results(start, end, keyword):
    info_raw_t=[]
    info_raw_l=[]
    end= end+ 1
    
    for i in range(start, end):
        number= str(10*i)
        html_keyword= urllib.parse.quote_plus(keyword)
        url = 'https://www.bing.com/search?q=' + html_keyword+ '&start='+number
        PATH= r"C:\Users\user\Data\webscraping_homepages\webdriver\chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(executable_path = PATH, options=options)
        driver.get(url)
        
            
        for element in driver.find_elements_by_xpath('//li[@class="b_algo"]'):
            title = element.find_element_by_xpath('.//h2').text
            link = element.find_element_by_xpath('.//h2/a').get_attribute('href')
            info_raw_l.append(link.lower())     
            info_raw_t.append(title.lower())
            
    return info_raw_l, info_raw_t

# find useful webpages (company homepage) from all the results 
# 80% of the results are garanteed to be company webpages 

def find_homepages(title, link):
    info=[]
    homepage=[]
    for i in range(len(title)):
        count= 0
        sub_link= link[i]
        count = sub_link.count("/")
        qm_find= sub_link.count('?')
        ul_find= sub_link.count('_')
        if count == 3 and qm_find==0 and ul_find==0:
            homepage.append(sub_link)
            info.append(title[i])
    return info, homepage 


def find_homepage_text(homepage):
    try:
        request= requests.get(homepage, headers={
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36"})         
        return request.text
    except:
        print('Unexpected error')

        
# find contact email from the homepages 

def find_contact_info(url, page_source):
    try:
        print('finding contact info for', url)
        EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    
        list_of_emails=[]
        for re_match in re.finditer(EMAIL_REGEX, page_source):
            list_of_emails.append(re_match.group())   
        if len(list_of_emails)==0:
            list_of_emails.append('No Found')
            
        duplicates=[]
        for i in list_of_emails:
          if list_of_emails.count(i)>1:
              if i not in duplicates:
                  duplicates.append(i)
    
        return duplicates
    except:
        pass 

def find_contact_list(link_h):
    try:
        contact=[]
        for url in link_h:
            page= find_homepage_text(url)
            email= find_contact_info(url, page)
            contact.append(email) 
    except:
        contact.append('')
        pass
    finally:
        return contact


