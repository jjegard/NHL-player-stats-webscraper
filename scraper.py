# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 17:22:17 2019

@author: John
"""

"""
The goal is to scrape the player and goalie stats from nhl.com from the 2018-19 NHL season that 
would be useful in a hockey pool and save this data in a CSV file.
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import os
import inspect

###########################FUNCTIONS########################

def getColumnHeaders(soup:BeautifulSoup):
    return 0;

###############MAIN########################
url = "http://www.nhl.com/stats/player?reportType=season&seasonFrom=20182019&seasonTo=20182019\
&gameType=2&filter=gamesPlayed,gte,1&sort=points"; 
                 

dir_path = os.path.dirname(os.path.realpath(__file__));
chromedriver = f'{dir_path}/chromedriver';
os.environ["webdriver.chrome.driver"] = chromedriver;


driver = webdriver.Chrome(executable_path=chromedriver);
driver.get(url);
html = driver.page_source;

soup = BeautifulSoup(html, "html5lib");
rows = soup.find_all("div", class_="rt-tr-group");

print(rows[0]);


driver.close();