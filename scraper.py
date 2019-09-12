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
import numpy as np
import pandas as pd

###########################FUNCTIONS########################

def getColumnIndices(table:BeautifulSoup, desiredStats:np.array)->list:
    """takes the desired stats np.array and returns a list of all the column indices for those player stats"""
    
    columnHeaders = table.select("div.rt-th.-cursor-pointer");
    
    colIndices = [];
    colIndexCounter = 0;
    
    for col in columnHeaders:
        if col.text.upper().strip() in np.char.upper(desiredStats):
            colIndices.append(colIndexCounter);
            
        colIndexCounter = colIndexCounter + 1;
    return colIndices;


def getPlayerStats(table:BeautifulSoup, desiredStats:np.array)->pd.DataFrame:
    """gets all the player stats from one page and puts it into a dataframe"""
    
    playerColIndices = getColumnIndices(table, desiredStats);
    rows = table.find_all("div", class_="rt-tr-group");
    
    playerStatsDF = pd.DataFrame(columns=desiredStats);
    for row in rows:
    #for row in [rows[0], rows[1]]: #DELETE
        individualPlayers = row.find_all("div", class_="rt-td");
        statsList = [];
        for individualPlayer in [individualPlayers[i] for i in playerColIndices]:
            statsList.append(individualPlayer.text);
        playerStatsDF.loc[len(playerStatsDF)] = statsList;
        
    return playerStatsDF;

###############MAIN########################
url = "http://www.nhl.com/stats/player?reportType=season&seasonFrom=20182019&seasonTo=20182019\
&gameType=2&filter=gamesPlayed,gte,1&sort=points";

desiredPlayerStats1 = np.array(["Player", "Team", "Pos", "GP", "G", "A", "P", "+/-", "PIM", "PPG", "PPP", "SHG",\
                      "SHP", "GWG", "S"]);
desiredPlayerStats2 = np.array(["Player", "Team", "HIT", "BLK"]);
desiredGoalieStats = ["Player", "Team", "GP", "GS", "W", "L", "OTL", "GA", "GAA", "SA", "SV", "S%", "SO"];
                 

dir_path = os.path.dirname(os.path.realpath(__file__));
chromedriver = f'{dir_path}/chromedriver';
os.environ["webdriver.chrome.driver"] = chromedriver;


driver = webdriver.Chrome(executable_path=chromedriver);
driver.get(url);
html = driver.page_source;

soup = BeautifulSoup(html, "html5lib");
table = soup.find("div", class_="rt-table");

playerStatsDF = getPlayerStats(table, desiredPlayerStats1);

driver.find_element_by_css_selector("div.-next .-btn").click();
#html = driver.page_source;
#soup = BeautifulSoup(html, "html5lib");
#table = soup.find("div", class_="rt-table");
#playerStatsDF = getPlayerStats(table, desiredPlayerStats1);


driver.close();