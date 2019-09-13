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
from selenium.webdriver.support.select import Select
import os
import numpy as np
import pandas as pd
import time

###########################FUNCTIONS########################
def createSoup(driver:webdriver)->BeautifulSoup:
    '''create soup and return the portion of the soup that contains the table where the
    the stats will be scraped from'''
    
    html = driver.page_source;
    soup = BeautifulSoup(html, "html5lib");
    table = soup.find("div", class_="rt-table");
    return table;


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


def getPlayerStatsOnCurrentPage(playerStatsDF:pd.DataFrame, table:BeautifulSoup, playerColIndices:list)->pd.DataFrame:
    """gets all the player stats from one page and puts it into a dataframe"""
    
   
    rows = table.find_all("div", class_="rt-tr-group");
    
    for row in rows:
    #for row in [rows[0], rows[1]]: #DELETE
        individualPlayers = row.find_all("div", class_="rt-td");
        statsList = [];
        for individualPlayer in [individualPlayers[i] for i in playerColIndices]:
            statsList.append(individualPlayer.text);
        playerStatsDF.loc[len(playerStatsDF)] = statsList;
        
    return playerStatsDF;


def getPlayerStats(driver:webdriver, desiredStats:np.array)->pd.DataFrame:
    countWhileLoop = 0; #DELETE
    #create empty dataframe for data to be appended to
    playerStatsDF = pd.DataFrame(columns=desiredStats);
    
    table = createSoup(driver);
#    return table; #DELETE
    playerColIndices = getColumnIndices(table, desiredStats);
    
    while True:
        countWhileLoop = countWhileLoop + 1; #DELETE
        
        getPlayerStatsOnCurrentPage(playerStatsDF, table, playerColIndices);
        
        if(not driver.find_element_by_css_selector("div.-next .-btn").is_enabled()):
            break;
        
        driver.find_element_by_css_selector("div.-next .-btn").click();
        table = createSoup(driver);
    print(countWhileLoop);
    
    return playerStatsDF;


def changeReportType(driver:webdriver, reportType:str):
    #Select report type from the drop down menu
    reportMenu = Select(driver.find_element_by_css_selector("div.filter--report select"));
    reportMenu.select_by_visible_text(reportType);
    #Click Run Report to generate Goalie Summary table
    driver.find_element_by_css_selector("div.toolbar__col.non-time-report-options button.go").click();

###############MAIN########################
url = "http://www.nhl.com/stats/player?reportType=season&seasonFrom=20182019&seasonTo=20182019\
&gameType=2&filter=gamesPlayed,gte,1&sort=points";

desiredPlayerStats1 = np.array(["Player", "Team", "Pos", "GP", "G", "A", "P", "+/-", "PIM", "PPG", "PPP", \
                                "SHG", "SHP", "GWG", "S"]);
desiredPlayerStats2 = np.array(["Player", "Team", "Hits", "BkS"]);
desiredGoalieStats = np.array(["Player", "Team", "GP", "GS", "W", "L", "OT", "SA", "Svs", "GA","Sv%", \
                               "GAA", "SO"]);
reportType = ["Hits, BkS, MsS, Gvwys, Tkwys (since 1997-98)", "Goalie Summary"];

dir_path = os.path.dirname(os.path.realpath(__file__));
chromedriver = f'{dir_path}/chromedriver';
os.environ["webdriver.chrome.driver"] = chromedriver;


driver = webdriver.Chrome(executable_path=chromedriver);
driver.get(url);

playerStatsDF1 = getPlayerStats(driver, desiredPlayerStats1);
changeReportType(driver, reportType[0]);
time.sleep(1);#Allows time for the javascript to run before grabbing the html
playerStatsDF2 = getPlayerStats(driver, desiredPlayerStats2);
changeReportType(driver, reportType[1]);
time.sleep(1);#Allows time for the javascript to run before grabbing the html
goalieStatsDF = getPlayerStats(driver, desiredGoalieStats);
driver.close();

playerStatsDF = pd.merge(playerStatsDF1, playerStatsDF2, on=[desiredPlayerStats1[0], desiredPlayerStats1[1]]);

playerStatsDF.to_csv("playerStats.csv", index=False);
goalieStatsDF.to_csv("goalieStats.csv", index=False);
