# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 17:22:17 2019

@author: John
"""

"""
The goal is to scrape the player and goalie stats from nhl.com from the 2018-19 NHL season that 
would be useful in a hockey pool and save this data in a CSV file.
"""

import urllib.request
from bs4 import BeautifulSoup


def getColumnHeaders(soup:BeautifulSoup):
    return 0;










url = "http://www.nhl.com/stats/player?reportType=season&seasonFrom=20182019&seasonTo=20182019\
&gameType=2&filter=gamesPlayed,gte,1&sort=points";

html = urllib.request.urlopen(url).read();
soup = BeautifulSoup(html, "html5lib");

#print(soup.prettify());

table = soup.find_all("tr");

print(len(table));
print(type(table));
print(type(soup));