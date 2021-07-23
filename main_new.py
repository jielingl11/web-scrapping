# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 19:05:43 2021

@author: user
"""

# scraping google result and determine the useful webpages

# import packages 

import urllib
import urllib.request as req
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import InvalidSessionIdException

# get all title and url of the google results from page one to page n 
# where n is a number you assign 

def google_results(pages, keyword):
    info_raw_t=[]
    info_raw_l=[]
    
    for i in range(1, pages):
        number= str(10*i)
        html_keyword= urllib.parse.quote_plus(keyword)
        url = 'https://www.google.com/search?q=' + html_keyword+ '&start='+number
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        
        
        for element in driver.find_elements_by_xpath('//div[@class="g"]'):
            title = element.find_element_by_xpath('.//h3').text
            link = element.find_element_by_xpath('.//div[@class="yuRUbf"]/a').get_attribute('href')
            info_raw_l.append(link.lower())     
            info_raw_t.append(title.lower())
            
    return info_raw_l, info_raw_t



def bing_results(pages, keyword):
    info_raw_t=[]
    info_raw_l=[]
    
    for i in range(10, pages):
        number= str(10*i)
        html_keyword= urllib.parse.quote_plus(keyword)
        url = 'https://www.bing.com/search?q=' + html_keyword+ '&start='+number
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
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
        


keyword= input('Please type the keyword you are looking for:\n')
pages= int(input('How many pages of results you want to scrap?\n')) + 1
browser= input('Searching with google or bing?(Please type google or bing)\n')
print('')
print('Searching for ' + keyword +'. Please wait...') 

if browser =='google':
    result= google_results(pages, keyword)
elif browser =='bing':
    result= bing_results(pages, keyword)
    
title= result[1]
link= result[0]

homepage= find_homepages(title, link)

title_h= homepage[0]
link_h= homepage[1]

contact_h= find_contact_list(link_h)

data= {'title':title_h, 'url': link_h,'contact': contact_h}
df= pd.DataFrame(data, columns=['title','url', 'contact'])

df['url']= df["url"].apply(lambda x: ",".join(x) if isinstance(x, list) else x)
df['contact']= df["contact"].apply(lambda x: ",".join(x) if isinstance(x, list) else x)

ask_save= input('Do you want to save as csv. file? y/n \n') 
if ask_save=='y':
    df.to_csv(r"C:\Users\user\OneDrive\Desktop\Turbine\data.csv")
    


#%%
        
# def contact_url_uk(url):
#     url_1= url+'contact/'
#     url_2= url+'contact-us/'
#     url_3= url+'about-us/'
#     return url, url_1, url_2, url_3


# def find_contact_list(link_h):
#     contact=[]
#     for url in link_h[3:]:
#         number= len(contact_url_uk(url))
#         count=0
#         for i in range(number):
#             url_test= contact_url_uk(url)[i]
#             page= find_homepage_text(url_test)
#             email= find_contact_info(url_test, page)
#             if len(email)==0:
#                 count+=1
#             if len(email)>0:
#                 contact.append(email)
#                 break
#         if count== number:
#             contact.append('No Found')  
#     return contact 

# contact_h= find_contact_list(link_h[3:])
