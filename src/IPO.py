import csv
import numpy as np

class IPO():
    def __init__(self, name,id,url):
        self.name = name
        self.id = id
        self.url = url
        self.ListedPrice = -1
        self.info = {}
        self.financialComp = {}
        self.PnL = {}
        self.cashFlow = {}
        self.balanceSheet = {}
        self.PE = 0
        self.PB = 0
        self.PS = 0

    def __str__(self):
        return "IPO Name\t:\t%s\nIPO Id\t:\t%s" % (self.name, self.id)

    def __repr__(self):
        return "IPO Name\t:\t%s\nIPO Id\t:\t%s" % (self.name, self.id)

    def addIPOInfo(self, infoList, labels):
        # print("infoList : ",infoList)
        # print("labels : ", labels)
        try:
            for i,label in enumerate(labels):
                if label not in self.info: #omit payee bank
                    self.info[label] = infoList[i]
        except Exception as e:
            print("IPO.addIPOInfo error: "),
            print(e)


    def addFinancialComp(self, financialCompList, labels):
        try:
            for i,label in enumerate(labels):
                if label not in self.financialComp:
                    self.financialComp[label] = financialCompList[i]
        except Exception as e:
            print("IPO.addFinancialComp error: "),
            print(e)


    def addPnL(self, PnLList, labels):
        # print("PnLList : ", PnLList)
        # print("labels : ", labels)
        try:
            for i,label in enumerate(labels):
                if label not in self.PnL:
                    self.PnL[label] = PnLList[i]
        except Exception as e:
            print("IPO.addPnL error: "),
            print(e)

    def addCashFlow(self, cashFlowList, labels):
        # print("cashFlowList : ",  cashFlowList)
        # print("labels : ", labels)
        try:
            for i,label in enumerate(labels):
                if label not in self.cashFlow:
                    self.cashFlow[label] = cashFlowList[i]
            temp = self.cashFlow["Year"]
            self.cashFlow["YearCashFlow"] = temp
            self.cashFlow.pop("Year", None)
        except Exception as e:
            print("IPO.addCashFlow error: "),
            print(e)


    def addBalanceSheet(self, balanceSheetList, labels):
        try:
            for i,label in enumerate(labels):
                if label not in self.balanceSheet:
                    self.balanceSheet[label] = balanceSheetList[i]

            temp = self.balanceSheet["Year"]
            self.balanceSheet["YearBalanceSheet"] = temp
            self.balanceSheet.pop("Year", None)
        except Exception as e:
            print("IPO.addBalanceSheet error: "),
            print(e)

    def getLabels(self):
        label = []
        label.append("Name")
        label.append("ID")
        label.append("Listed Price")
        for k in self.info.keys():
            label.append(k)
        for k in self.financialComp.keys():
            label.append(k)
        for k in self.PnL.keys():
            label.append(k)
        for k in self.cashFlow.keys():
            label.append(k)
        for k in self.balanceSheet.keys():
            label.append(k)

        label.append("PE Ratio")
        label.append("PB Ratio")
        # label.append("PS Ratio")
        return label

    def getValues(self):
        values = []
        values.append(self.name)
        values.append(self.id)
        values.append(self.ListedPrice)
        for v in self.info.values():
            values.append(v)
        for v in self.financialComp.values():
            values.append(v)
        for v in self.PnL.values():
            values.append(v)
        for v in self.cashFlow.values():
            values.append(v)
        for v in self.balanceSheet.values():
            values.append(v)
        values.append(self.PE)
        values.append(self.PB)
        return values

    def validIPO(self):
        return True
        if not (bool(self.info) or bool(self.financialComp) or bool(self.PnL)):
            print("info or fin or pnl empty")
            return False
        elif len(self.info.keys()) != 11:
            print("info keys not = 11")
            print(len(self.info.keys()))
            print(self.info.keys())
            return False
        else:
            return True


    def formatAttributes(self):
        #IPO ID
        if len(self.id) != 4:
            # id = self.id.zfill(4)
            id = self.id
            # print(id[1:])
            self.id = "HKG:" + str(id[1:])

        # Global offered shares
        try:
            rename = self.info['No. of Global Offered Shares2']
            self.info['No. of Global Offered Shares'] = rename
            self.info.pop('No. of Global Offered Shares2')
        except Exception as e:
            print("global offered shares error")
            for k in self.info.keys():
                print(k)
            print("asdf")




        #Lot Size
        try:
            self.info["Lot Size"] = float(self.info["Lot Size"].replace(",",""))
        except Exception as e:
            print(e)
            print(self.id)

        # Listed Price
        if self.ListedPrice != "N/A":
            self.ListedPrice = float(self.ListedPrice.replace(",",""))

        # Offer price split into upper and lower
        try:
            split = self.info["Offer Price"].split("-")
            if len(split) == 2:
                lower = float(split[0])
                upper = float(split[1])
            else:
                lower = "N/A"
                upper = "N/A"

            self.info.pop('Offer Price', None)
            self.info['Lower Price'] = lower
            self.info['Upper Price'] = upper
        except Exception as e:
            print("split offer price error!")
            print(e)
        #book value, just delete atm
        self.info.pop('Book Value')

        #Market Cap
        if self.info["Market Cap"].strip() != "N/A":
            split = self.info["Market Cap"].split("-")
            if len(split) == 2:
                lower = float(split[0].replace(",",""))
                upper = float(split[1].replace(",",""))

                mean = np.mean([lower, upper])
                spread = (upper-mean)/mean
            elif split[0] == "N/A":
                mean = "N/A"
                spread = "N/A"
            else:
                mean = float(split[0].replace(",", ""))
                spread = 0
            self.info.pop('Market Cap', None)
            self.info['Market Cap mean'] = mean
            self.info['Market Cap spread (%)'] = spread
        else:
            self.info.pop('Market Cap', None)
            self.info['Market Cap mean'] = "N/A"
            self.info['Market Cap spread (%)'] = "N/A"

        # No. of Global Offered Shares
        num = self.info["No. of Global Offered Shares"]
        if num.strip() != "N/A":
            self.info["No. of Global Offered Shares"] = float(num.replace(",",""))
        else:
            pass

        # No. of HK Offered Shares2
        split = self.info["No. of HK Offered Shares2"].split("(")
        if len(split) == 2:
            num = split[0].replace(",","")
            percentage = float(split[1].strip("%)"))/100
        else:
            num = "N/A"
            percentage = "N/A"
        self.info["No. of HK Offered Shares"] = num
        self.info["No. of HK Offered Shares(%)"] = percentage
        self.info.pop("No. of HK Offered Shares2", None)

        # No. of International Placing Shares2
        split = self.info["No. of International Placing Shares2"].split("(")
        if len(split) == 2:
            num = split[0].replace(",", "")
            percentage = float(split[1].strip("%)")) / 100
        else:
            num = "N/A"
            percentage = "N/A"
        self.info["No. of International Placing Shares"] = num
        self.info["No. of International Placing Shares(%)"] = percentage
        self.info.pop("No. of International Placing Shares2", None)

        #start dealing with multiyear financialComp
        try:
            for k,v in self.financialComp.items():
                if k != "YearFinancialComp":
                    newArr = [float(x.replace(",","")) for x in v if x != "-" if x != "N/A"]
                    # at the moment we aggregate to a mean, later on think of a way to describe the trend
                    if all(x==0 for x in newArr):
                        mean = 0
                    else:
                        mean = np.mean(newArr)
                    self.financialComp[k] = mean
        except Exception as e:
            print("multiyear financialComp data error")
            print(e)

        # deal with multiyear PnL data
        try:
            for k,v in self.PnL.items():
                if not (k == "YearPnL" or k == "Currency" or k == "Unit"):
                    # some arrays have k behind numbers, idk why
                    newArr = [float(x.replace(",","")) for x in v if x != "-" if x != "N/A" if x[-1] != "k" if x[-1] != "K"] # atm this discards invalid values ("-"), this doesn't matter atm since we are taking the mean, but we need to handle this when we need to measure trend possibly? (human may only observe change disregarding years)
                    # print(newArr)
                    # at the moment we aggregate to a mean, later on think of a way to describe the trend
                    if all(x==0 for x in newArr):
                        mean = 0
                    else:
                        mean = np.mean(newArr)
                    self.PnL[k] = mean
        except Exception as e:
            print("multiyear PnL data error")
            print(e)

        # deal with multiyear cashFlow data
        try:
            for k, v in self.cashFlow.items():
                if not (k == "YearCashFlow" or k == "Currency" or k == "Unit"):
                    # some arrays have k behind numbers, idk why
                    newArr = [float(x.replace(",", "")) for x in v if x != "-" if x != "N/A" if x[-1] != "k" if x[
                        -1] != "K"]  # atm this discards invalid values ("-"), this doesn't matter atm since we are taking the mean, but we need to handle this when we need to measure trend possibly? (human may only observe change disregarding years)
                    # print(newArr)
                    # at the moment we aggregate to a mean, later on think of a way to describe the trend
                    if all(x == 0 for x in newArr):
                        mean = 0
                    else:
                        mean = np.mean(newArr)
                    self.cashFlow[k] = mean
        except Exception as e:
            print("multiyear cashFlow data error")
            print(e)

        # deal with multiyear balanceSheet data
        try:
            for k, v in self.balanceSheet.items():
                if not (k == "YearBalanceSheet" or k == "Currency" or k == "Unit"):
                    # some arrays have k behind numbers, idk why
                    newArr = [float(x.replace(",", "")) for x in v if x != "-" if x != "N/A" if x[-1] != "k" if x[
                        -1] != "K"]  # atm this discards invalid values ("-"), this doesn't matter atm since we are taking the mean, but we need to handle this when we need to measure trend possibly? (human may only observe change disregarding years)
                    # print(newArr)
                    # at the moment we aggregate to a mean, later on think of a way to describe the trend
                    if all(x == 0 for x in newArr):
                        mean = 0
                    else:
                        mean = np.mean(newArr)
                    self.balanceSheet[k] = mean
        except Exception as e:
            print("multiyear balanceSheet data error")
            print(e)

        # PnL currency conversion
        try:
            currency = self.PnL['Currency']
            conversionDict = {  "AUD":  5.7,
                                "EUR":  8.8,
                                "HKD":  1.0,
                                "MOP":  1.0,
                                "MYR":  1.9,
                                "RM" :  1.9,
                                "RMB":  1.15,
                                "USD":  7.8,
                                "SGD":  5.82,
                                "THB":  0.26,}

            if max(currency, key = currency.count) in conversionDict.keys():
                conversionRate = conversionDict[max(currency, key = currency.count)]
                for k,v in self.PnL.items():
                    if v != "N/A" and k != "YearPnL" and k != "Currency" and k != "Unit":
                        self.PnL[k] = v*conversionRate*1000

        except Exception as e:
            print("PnL Currency conversion error: ",  end=" ")
            print(e)

        # CashFlow currency conversion
        try:
            currency = self.cashFlow['Currency']
            conversionDict = {  "AUD":  5.7,
                                "EUR":  8.8,
                                "HKD":  1.0,
                                "MOP":  1.0,
                                "MYR":  1.9,
                                "RM" :  1.9,
                                "RMB":  1.15,
                                "USD":  7.8,
                                "SGD":  5.82,
                                "THB":  0.26,}

            if max(currency, key = currency.count) in conversionDict.keys():
                conversionRate = conversionDict[max(currency, key = currency.count)]
                for k,v in self.cashFlow.items():
                    if v != "N/A" and k != "YearCashFlow" and k != "Currency" and k != "Unit":
                        self.cashFlow[k] = v*conversionRate*1000

        except Exception as e:
            print("cashFlow Currency conversion error: ",  end=" ")
            print(e)

        # BalanceSheet currency conversion
        try:
            currency = self.balanceSheet['Currency']
            conversionDict = {  "AUD":  5.7,
                                "EUR":  8.8,
                                "HKD":  1.0,
                                "MOP":  1.0,
                                "MYR":  1.9,
                                "RM" :  1.9,
                                "RMB":  1.15,
                                "USD":  7.8,
                                "SGD":  5.82,
                                "THB":  0.26,}

            if max(currency, key = currency.count) in conversionDict.keys():
                conversionRate = conversionDict[max(currency, key = currency.count)]
                for k,v in self.balanceSheet.items():
                    if v != "N/A" and k != "YearBalanceSheet" and k != "Currency" and k != "Unit":
                        self.balanceSheet[k] = v*conversionRate*1000

        except Exception as e:
            print("balanceSheet Currency conversion error: ",  end=" ")
            print(e)


        # PE ratio
        try:
            valuePerShare = np.mean([float(self.info['Upper Price']),float(self.info['Lower Price'])])
            sharesOutstanding = self.info['No. of Global Offered Shares']#/self.info['Lot Size']
            earningsPerShare = self.PnL['Profit Attributable to Shareholders'] / sharesOutstanding
            self.PE = valuePerShare / earningsPerShare
        except Exception as e:
            print("PE ratio error!")
            print(e)
            self.PE = 0

        # PB ratio
        try:
            valuePerShare = np.mean([float(self.info['Upper Price']), float(self.info['Lower Price'])])
            sharesOutstanding = self.info['No. of Global Offered Shares'] #/ self.info['Lot Size']
            bookValuePerShare = (self.balanceSheet['Total Assets'] - (self.balanceSheet['Other Long Term Liabilities'] + self.balanceSheet['Current Liabilities']))/ sharesOutstanding
            self.PB = valuePerShare/bookValuePerShare
        except Exception as e:
            print("PB ratio erro!")
            print(e)
            self.PB = 0
        # PS ratio (N/A)