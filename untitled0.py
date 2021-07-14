# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 13:11:23 2021

@author: user
"""

from selenium import webdriver
import urllib
from bs4 import BeautifulSoup
import pandas as pd
from selenium.common.exceptions import InvalidSessionIdException
import time
import requests

URL = 'https://www.dnb.com/business-directory/company-information.aquaculture.gb.html?page=4'

# companies= delete_dash(find_list(URL))
page = requests.get(URL, headers={
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36"})
soup = BeautifulSoup(page.content, "html.parser")
items= soup.find_all('div',class_='col-md-12 data')

companies=[]

for item in items:
    name= item.find('a')
    find= str(name.text.strip())
    companies.append(find.lower())

#%%
from selenium import webdriver
import pandas as pd

def find_list(URL):
    companies_list = requests.get(URL)
    page = requests.get(URL, headers={
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36"})
    soup = BeautifulSoup(page.content, "html.parser")
    items= soup.find_all('h2',class_='h2 m-b-0')
    
    companies=[]
    
    for item in items:
        name= item.find('a')
        find= str(name.text.strip())
        companies.append(find.lower())

    return companies


def delete_dash(companies):

    companies_new=[]
    for company in companies:
        if company.find('-') == 0:
            companies_new.append(company)
        else:
            splitting= company.split('-')
            companies_new.append(splitting[0])
            
    return companies_new


def url(keyword):
    html_keyword= urllib.parse.quote_plus(keyword)
    google_url = "https://www.google.com/search?q=" + html_keyword
    return google_url



def google_search(google_url, keyword, Open= False):
    
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(options=option)
    driver.get(google_url)
    
    if Open:
        driver = webdriver.Chrome()
        driver.get(google_url)
        time.sleep(1)
        # driver.close()
        
    info_raw=[]
    for element in driver.find_elements_by_xpath('//div[@class="g"]'):
        title = element.find_element_by_xpath('.//h3').text
        link = element.find_element_by_xpath('.//div[@class="yuRUbf"]/a').get_attribute('href')
        info_raw.append([keyword, title.lower().replace("\n",""), link.lower().replace("\n","")])        
        info= pd.DataFrame(info_raw[:3][:])
    return info

def save_csv(info):
    info.to_csv(r'C:\Users\user\OneDrive\Desktop\Turbine\company2.csv') 
    

# determine whether the page is the homepage of the company 

def find_homepage(result):
    homepage=[]
    for i in range(3):
        count= 0
        sub_link= result[2][i]
        count = sub_link.count("/")
        
        if count == 3:
            homepage.append(sub_link)
    return homepage

# get into homepage 
def find_homepage_text(homepage):
    # for home in homepage:
    request= requests.get(homepage, headers={
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36"})
    
    return request.text


# calculating score to determine whether to reserve the data point 
def calculation(page):
    score= 0
    # keyword 1
    keyword1= page.count('aquaculture')
    keyword1_1= page.count('aquafarming')
    score= keyword1+ keyword1_1
    
    # keyword 2
    keyword2= page.count('farming')
    keyword2_1= page.count('farm')
    species= ['fish', 'shrimp', 'prawn', 'salmon', 'crap', 'mussel', 
              'oyster', 'seaweed', 'algae', 'lobster']
    species_type=[]
    count=0
    for s in species:
        keyword2_2= page.count(s)
        if keyword2_2>= 2: 
            species_type.append(s)
            count+=1
    score= score+ keyword2+ keyword2_1 + count
    
    # keyword 3
    keyword3= page.count('equipment')
    score += keyword3
    
    # keyword 4
    keyword4= page.count('marine')
    score += keyword4
    
    company_new=[]
    if score > 5:
        company_new.append(keyword)
    return score, company_new



URL=[]

for keyword in companies:
    print('searching for', keyword, '...')
    html_keyword= urllib.parse.quote_plus(keyword)
    url = "https://www.google.com/search?q=" + html_keyword
    google_result= google_search(url, keyword)
    homepage= find_homepage(google_result)    
    URL.append(homepage)

#%%    
data2= {'company': companies[0:30],
       'url': URL}
df2= pd.DataFrame(data2, columns=['company','url'])

df2['url']= df2["url"].apply(lambda x: ",".join(x) if isinstance(x, list) else x)


#%%

save1= save_csv(df2)



#%% find contact info 
import re
from selenium import webdriver
import numpy as np

def find_homepage_text(homepage):
    # for home in homepage:
    request= requests.get(homepage, headers={
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36"})
    
    return request.text



def find_contact_info(url, page_source):
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

contact2=[]
homepage= df2['url'].tolist()
for url in homepage:
    if len(url)==0:
        contact2.append('No Found')
    else:
        try:
            count= url.count(',')
            if count ==0:
                page= find_homepage_text(url)
                email= find_contact_info(url, page)
                contact2.append(email)
            if count >=1:
                page= find_homepage_text(url.split(',')[0])
                email= find_contact_info(url.split(',')[0], page)
                contact2.append(email)
        except:
            contact2.append('No Found')
            pass
   
#%%

data2= {'company': companies,
       'url': URL, 'contact': contact2}
df2= pd.DataFrame(data2, columns=['company','url', 'contact'])

df2['url']= df2["url"].apply(lambda x: ",".join(x) if isinstance(x, list) else x)
df2['contact']= df2['contact'].apply(lambda x: ",".join(x) if isinstance(x, list) else x)

df2.to_csv(r'C:\Users\user\OneDrive\Desktop\Turbine\company3.csv')



#%%


