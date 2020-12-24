from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from IPO import *
import time
import sys
import re
import csv
import pickle

# class IPOScraper():
#     def __init__(self):
#         chromeDriverPath = ()
#         chromeOptions = Options()
#         chromeOptions.add_argument("--headless")
#         self.driver = webdriver.Chrome(executable_path="C:/Users/thtan/PycharmProjects/IPO/webDriver/chromedriver.exe",
#                                        options=chromeOptions)
#
#     def  initWebDriver(self):
#         pass




def getIPOInfo(currentIPO):
    button = driver.find_element_by_xpath('//div[text() = "IPO Info"]')
    button.click()
    WebDriverWait(driver,10)
    elements = driver.find_elements_by_xpath('//div[@class="mar30B comm-panel"][1]//tr')
    desiredAttributes = ["Lot Size",
                         "Offer Price",
                         "Book Value",
                         "Market Cap",
                         "Listing Date",
                         "No. of Global Offered Shares2",
                         "No. of HK Offered Shares2",
                         "No. of International Placing Shares2",
                         "Underwriter(s)",
                         "Sponsor(s)"]
    try:
        data = []
        for i, element in enumerate(elements):
            if i < len(desiredAttributes):
                attribute = desiredAttributes[i]
                data.append(element.text.split(attribute)[1].strip())
        currentIPO.addIPOInfo(data, desiredAttributes)
        return True
    except:
        print("packAttributes error")
        return False

def getIndustryComp(currentIPO):
    button = driver.find_element_by_xpath('//div[text() = "Industry Comp"]')
    button.click()
    WebDriverWait(driver,10)

def getFinancialComp(currentIPO):
    button = driver.find_element_by_xpath('//div[text() = "Financial Comp"]')
    button.click()
    WebDriverWait(driver,10)

    columnHeader = ["Year",
                    "Current Ratio (X)",
                    "Quick Ratio (X)",
                    "Long Term Debt/Equity (%)",
                    "Total Debt/Equity (%)",
                    "Total Debt/Capital Employed (%)",
                    "Return on Equity (%)",
                    "Return on Capital Employ (%)",
                    "Return on Total Assets (%)",
                    "Operating Profit Margin (%)",
                    "Pre-tax Profit Margin (%)",
                    "Net Profit Margin (%)",
                    "Inventory Turnover (X)",
                    "Dividend Payout (%)"]
    years = driver.find_element_by_xpath("//tr[@ref='FR_Field_NB_1']").text.split()
    years = years[:-1]  #discard the compare column
    years = [x for x in years if x != "Average" if x != "Year"]
    # print(years)
    try:
        data = []
        data.append(years)
        for row in range(2,15):
            elements = driver.find_elements_by_xpath("//tr[@ref='FR_Field_NB_"+ str(row) + "']")

            for element in elements:
                # print(element.text)
                element = element.text.split(columnHeader[row-1])[1].strip() #remove column header
                element = element.split()[:len(years)] #discard average and compare column
                data.append(element)

        currentIPO.addFinancialComp(data,columnHeader)
        return True
    except Exception as e:
        print("Financial Comp error")
        print(e)
        return False
def getPnL(currentIPO):
    button = driver.find_element_by_xpath('//div[text() = "Profit & Loss"]')
    button.click()
    WebDriverWait(driver,10)
    columnHeader = ["Year",
                    "Currency",
                    "Unit",
                    "Turnover",
                    "Operating Profit",
                    "Exceptional Items",
                    "Associates",
                    "Pre-tax Operating Profit",
                    "Taxation",
                    "Minority Interests",
                    "Profit Attributable to Shareholders",
                    "Year",
                    "Depreciation",
                    "Interest Paid",
                    "Interest Capitalized",
                    "Disposal / Revaluation of Fixed Assets",
                    "Taxation Rate (%)",
                    "Turnover Growth (%)",
                    "Growth of Profit Attributable to Shareholders (%)"]
    # //tr[@ref = starts-with(text(),'PL_Field_NB_4')]
    elements = driver.find_elements_by_xpath("//tr[@ref]")

    try:
        data = []
        for i,element in enumerate(elements):
            element = element.text.split(columnHeader[i])[1].strip()    #strip header column
            element = element.split()   #separate
            data.append(element)
        currentIPO.addPnL(data,columnHeader)
        return True
    except Exception as e:
        print("get PnL error!")
        print(e)
        return False

def getCashFlow(currentIPO):
    button = driver.find_element_by_xpath('//div[text() = "Cash Flow"]')
    button.click()
    WebDriverWait(driver,10)

def getBalanceSheet(currentIPO):
    button = driver.find_element_by_xpath('//div[text() = "Balance Sheet"]')
    button.click()
    WebDriverWait(driver,10)

def getAllIPOAttributes(IPODict):
    i = 0
    for id,ipo_ in IPODict.items():
        i += 1
        try:
            print(100*i/len(IPODict), "%\tgetting info for IPO : ", id)
            driver.get(ipo_.url)
            getIPOInfo(ipo_)
            driver.get(ipo_.url)
            getFinancialComp(ipo_)
            driver.get(ipo_.url)
            getPnL(ipo_)
        except Exception as e:
            print("error getting attribute for IPO ", id)
            print(e)
            continue

def getIPOFromPage(IPODict):
    elements = driver.find_elements_by_xpath("//div[@id='IPOListed']//table[@class='ns2 dataTable']//a[not(@class)]")
    for element in elements:
        IPOName = element.text
        IPOUrl = element.get_attribute('href')
        IPOId = IPOUrl.split("?symbol=")[1].split("#info")[0]

        if IPOId not in IPODict:
            IPODict[IPOId] = IPO(IPOName, IPOId, IPOUrl)
    return True

def getAllListedIPO(IPODict):
    totalPages = 2
    for pageIdx in range(1,totalPages+1):
        pageUrl = "http://www.aastocks.com/en/stocks/market/ipo/listedipo.aspx?s=3&o=0&page="+str(pageIdx)
        driver.get(pageUrl)
        try:
            elementPresent = EC.presence_of_element_located((By.ID, 'IPOListed'))
            WebDriverWait(driver, delay).until(elementPresent)
            print("Reading page ", pageIdx)
        except TimeoutException:
            print("Loading took too much time!")
            continue
        getIPOFromPage(IPODict)



if __name__ == "__main__":

    #driver init
    chromeDriverPath = ("C:/Users/thtan/PycharmProjects/IPO/webDriver/chromedriver.exe")
    chromeOptions = Options()
    chromeOptions.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=chromeDriverPath, options=chromeOptions)

    # driver.get("http://www.aastocks.com/en/stocks/market/ipo/listedipo.aspx?s=3&o=0&page=1")
    element = WebDriverWait(driver,10)
    #
    #
    # IPODict = {}
    # getAllListedIPO(IPODict)
    #
    # print(IPODict)
    # for k,v in IPODict.items():
    #     print(v)
    # print(len(IPODict))
    IPODict = {}
    getAllListedIPO(IPODict)
    # for k,v in IPODict.items():
    #     print(k)

    # currentIPO = IPO("test","test","test")
    # driver.get("http://www.aastocks.com/en/stocks/market/ipo/upcomingipo/company-summary?symbol=02142&s=3&o=1#info")
    # getPnL(currentIPO)
    # currentIPO.printPnL()
    getAllIPOAttributes(IPODict)
    driver.close()


    with open('scrappedIPOs.pkl', 'wb') as output:
        pickle.dump(IPODict, output, protocol=pickle.HIGHEST_PROTOCOL)
        # for ipo in IPODict:
        #     pickle.dump(ipo, output, pickle.HIGHEST_PROTOCOL)
    print("finish writing to pickle file")