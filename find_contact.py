# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 16:12:10 2021

@author: user
"""
import scraping as sp

def find_contact_list(link_h):
    try:
        contact=[]
        for url in link_h:
            page= sp.find_homepage_text(url)
            email= sp.find_contact_info(url, page)
            contact.append(email) 
    except:
        contact.append('')
        pass
    finally:
        return 
    
def add1(a,b):
    return a+b