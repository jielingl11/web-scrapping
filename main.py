# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 19:05:43 2021

@author: user
"""



import pandas as pd
import scraping as sp
import find_contact as fc




keyword= input('Please type the keyword you are looking for:\n')
print('Please type the start and the end of the page you want to scrap:')
start= int(input('Start with Page (Type a number)\n'))
end= int(input('End with Page (Type a number)\n'))
browser= input('Searching with google or bing?(Please type google or bing)\n')
print('')
print('Searching for ' + keyword +'. Please wait...') 

if browser =='google':
    result= sp.google_results(start, end, keyword)
elif browser =='bing':
    result= sp.bing_results(start, end, keyword)
    
title= result[1]
link= result[0]

homepage= sp.find_homepages(title, link)

title_h= homepage[0]
link_h= homepage[1]

contact_h= fc.find_contact_list(link_h)

data= {'title':title_h, 'url': link_h,'contact': contact_h}
df= pd.DataFrame(data, columns=['title','url', 'contact'])

df['url']= df["url"].apply(lambda x: ",".join(x) if isinstance(x, list) else x)
df['contact']= df["contact"].apply(lambda x: ",".join(x) if isinstance(x, list) else x)

ask_save= input('Do you want to save as csv. file? y/n \n') 
if ask_save=='y':
    df.to_csv(r"C:\Users\user\OneDrive\Desktop\Turbine\data.csv")

