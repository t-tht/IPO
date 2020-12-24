from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from IPO import *
import pickle
import time


def getIPOInfo(currentIPO):
    # button = driver.find_element_by_xpath('//div[@class="con" and text() = "IPO Info"]')
    # button.click()
    # WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
    button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="con" and text() = "IPO Info"]')))
    button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="mar30B comm-panel"][1]//tr[not(ancestor::tr)]')))
    elements = driver.find_elements_by_xpath('//div[@class="mar30B comm-panel"][1]//tr[not(ancestor::tr)]')

    columnHeader = ["Lot Size",
                         "Offer Price",
                         "Book Value",
                         "Market Cap",
                         "Listing Date",
                         "No. of Global Offered Shares2",
                         "No. of HK Offered Shares2",
                         "No. of International Placing Shares2",
                         "Underwriter(s)",
                         "Sponsor(s)",
                         "Payee Bank"]
    try:
        data = []
        for i, element in enumerate(elements):
            element = element.text.split(columnHeader[i])[1]
            # print(element)
            data.append(element)

        currentIPO.addIPOInfo(data, columnHeader)
        return True
    except Exception as e:
        print("getIPOInfo error: "),
        print(e)
        return False


def getIndustryComp(currentIPO):
    button = driver.find_element_by_xpath('//div[text() = "Industry Comp"]')
    button.click()
    WebDriverWait(driver,10)

def getFinancialComp(currentIPO):
    button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="con" and text() = "Financial Comp"]')))
    button.click()
    WebDriverWait(driver,10)
    try:
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
        # years = driver.find_element_by_xpath("//tr[@ref='FR_Field_NB_1']").text.split()
        # years = years[:-1]  #discard the compare column
        # years = [x for x in years if x != "Average" if x != "Year"]
        data = []
        # data.append(years)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@class='ns5 mar10T']//tr[@ref]")))
        elements = driver.find_elements_by_xpath("//table[@class='ns5 mar10T']//tr[@ref]")

        years = driver.find_element_by_xpath("//table[@class='ns5 mar10T']//tr[@ref][1]").text
        years = years.split("Year")[1].split("Average")[0].strip().split()
        data.append(years)

        for i,element in enumerate(elements):
            if i != 0:
                element = element.text.split(columnHeader[i])[1].strip() #remove column header
                element = element.split()[:len(years)] #discard average and compare column
                data.append(element)

        columnHeader[0] = "YearFinancialComp"
        currentIPO.addFinancialComp(data,columnHeader)
        return True
    except Exception as e:
        print("getFinancialComp error: "),
        print(e)
        return False

def getPnL(currentIPO):
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="con" and text() = "Profit & Loss"]')))
    # button = driver.find_element_by_xpath('//div[text() = "Profit & Loss"]')
    button.click()
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
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[@ref]")))
    elements = driver.find_elements_by_xpath("//tr[@ref]")

    try:
        data = []
        for i,element in enumerate(elements):
            element = element.text.split(columnHeader[i])[1].strip()    #strip header column
            element = element.split()   #separate
            data.append(element)
        columnHeader[0] = "YearPnL"
        columnHeader[11] = "YearPnL"
        currentIPO.addPnL(data,columnHeader)
        return True
    except Exception as e:
        print("getPnL error: "),
        print(e)
        return False

def getCashFlow(currentIPO):
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="con" and text() = "Cash Flow"]')))
    # button = driver.find_element_by_xpath('//div[text() = "Cash Flow"]')
    button.click()
    WebDriverWait(driver,10)

    columnHeader = ["Year",
                    "Currency",
                    "Unit",
                    "Net Cash Flow from Operating Activities",
                    "Net Cash Flow from Return on Investments & Servicing of Finance",
                    "Interest Received",
                    "Interest Paid",
                    "Dividend Received",
                    "Dividend Paid",
                    "Others", #9
                    "Refunded/Taxes(Paid)",
                    "Net Cash Flow from Investing Activities",
                    "Additions to Fixed Assets",
                    "Disposal of Fixed Assets",
                    "Increase in Investments",
                    "Decrease in Investments",
                    "Net Cash Flow with Related Parties",
                    "Others", #17
                    "Net Cash Flow before Financing Activities",
                    "Net Cash Flow from Financing Activities",
                    "New Loans",
                    "Loans Repayment",
                    "Fixed Interest/Debt Instruments Financing",
                    "Repayment of Fixed Interest/Debt Instruments Financing",
                    "Equity Financing",
                    "Net Cash Flow with Related Parties",
                    "Others", #26
                    "Increase(Decrease) in Cash & Cash Equivalents",
                    "Cash & Cash Equivalents at Beginning of Year",
                    "Net Cash Flow due to Change in Exchange Rate/Others",
                    "Cash & Cash Equivalents at End of Year",]
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table[@class='ns5 mar10T']//tr")))
    elements = driver.find_elements_by_xpath('//table[@class="ns5 mar10T"]//tr')
    try:
        data = []
        for i, element in enumerate(elements):
            # print(i, " ", element.text)
            element = element.text.split(columnHeader[i])[1].strip()
            element = element.split()
            data.append(element)

        columnHeader[9] = "Net Cash Flow from Return on Investments & Servicing of Finance : Others"
        columnHeader[17] = "Net Cash Flow from Investing Activities : Others"
        columnHeader[26] = "Net Cash Flow from Financing Activities : Others"
        currentIPO.addCashFlow(data, columnHeader)
        return True

    except Exception as e:
        print("getCashFlow error: "),
        print(e)
        return False

def getBalanceSheet(currentIPO):
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="con" and text() = "Balance Sheet"]')))
    button.click()
    WebDriverWait(driver,10)
    columnHeader = ["Year",
                    "Currency",
                    "Unit",
                    "Fixed Assets",
                    "Investments",
                    "Current Assets",
                    "Other Assets",
                    "Total Assets",
                    "Long Term Debt",
                    "Other Long Term Liabilities",
                    "Current Liabilities",
                    "Share Capital",
                    "Reserves",
                    "Equity",
                    "Year",
                    "Inventory",
                    "Cash in Hand",
                    "Short Term Debt",
                    "Total Debt",]

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table[@class='ns5 mar10T']//tr")))
    elements = driver.find_elements_by_xpath('//table[@class="ns5 mar10T"]//tr')
    try:
        data = []
        for i, element in enumerate(elements):
            element = element.text.split(columnHeader[i])[1].strip()
            element = element.split()
            data.append(element)

        currentIPO.addBalanceSheet(data, columnHeader)
        return True

    except Exception as e:
        print("getBalanceSheet error: "),
        print(e)
        return False

def getAllIPOAttributes(IPODict):
    i = 0
    blackList = []

    for id,ipo_ in IPODict.items():
        i += 1
        try:
            print(100*i/len(IPODict), "%\tgetting info for IPO : ", id, "====================")
            driver.get(ipo_.url)
            getIPOInfo(ipo_)
            # driver.get(ipo_.url)
            getFinancialComp(ipo_)
            # driver.get(ipo_.url)
            getPnL(ipo_)
            # driver.get(ipo_.url)
            getCashFlow(ipo_)
            # driver.get(ipo_.url)
            getBalanceSheet(ipo_)
        except Exception as e:
            print("error getting all attribute for IPO ", id, ": "),
            print(e)
            blackList.append(id)
            continue

    for invalidIPOId in blackList:
        IPODict.pop(invalidIPOId)

def getIPOFromPage(IPODict):
    elements = driver.find_elements_by_xpath("//div[@id='IPOListed']//table[@class='ns2 dataTable']//a[not(@class)]")
    prices = driver.find_elements_by_xpath("//tr//td[@class='txt_r cls'][5]")
    for i,element in enumerate(elements):
        IPOName = element.text
        IPOUrl = element.get_attribute('href')
        IPOId = IPOUrl.split("?symbol=")[1].split("#info")[0]

        ListedPrice = prices[i].text

        if IPOId not in IPODict:
            IPODict[IPOId] = IPO(IPOName, IPOId, IPOUrl)
            IPODict[IPOId].ListedPrice = ListedPrice
    return True

def getAllListedIPO(IPODict):
    # totalPages = 2 # for testing
    totalPages = 28  # for scraping, check if there is actually 28 pages max each time
    for pageIdx in range(2,totalPages+1):
        pageUrl = "http://www.aastocks.com/en/stocks/market/ipo/listedipo.aspx?s=3&o=0&page="+str(pageIdx)
        driver.get(pageUrl)
        delay=1
        try:
            elementPresent = EC.presence_of_element_located((By.ID, 'IPOListed'))
            WebDriverWait(driver, delay).until(elementPresent)
            print("Reading page ", pageIdx, " of ", totalPages)
        except TimeoutException:
            print("Loading took too much time!")
            continue
        getIPOFromPage(IPODict)



if __name__ == "__main__":

    #driver init
    chromeDriverPath = ("C:/Users/thtan/PycharmProjects/IPO/webDriver/chromedriver.exe") #home
    # chromeDriverPath = ("C:/Users/bitex2020/Documents/webdriver/chromedriver.exe")  #bitex
    chromeOptions = Options()
    # chromeOptions.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=chromeDriverPath, options=chromeOptions)



    element = WebDriverWait(driver,10)
    IPODict = {}
    getAllListedIPO(IPODict)
    getAllIPOAttributes(IPODict)
    driver.close()


    with open('scrappedIPOsFull.pkl', 'wb') as output:
        pickle.dump(IPODict, output, protocol=pickle.HIGHEST_PROTOCOL)
    print("finish writing to pickle file")