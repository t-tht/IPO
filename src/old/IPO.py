import csv
import numpy as np

class IPO():
    def __init__(self, name,id,url):
        self.name = name
        self.id = id
        self.url = url
        self.info = {}
        self.financialComp = {}
        self.PnL = {}

    def __str__(self):
        return "IPO Name\t:\t%s\nIPO Id\t:\t%s" % (self.name, self.id)

    def __repr__(self):
        return "IPO Name\t:\t%s\nIPO Id\t:\t%s" % (self.name, self.id)

    def addIPOInfo(self, infoList, labels):
        for i,label in enumerate(labels):
            if label not in self.info:
                self.info[label] = infoList[i]
        # self.LotSize = IPOInfoList[0]
        # self.OfferPrice = IPOInfoList[1]
        # self.BookValue = IPOInfoList[2]
        # self.MarketCap = IPOInfoList[3]
        # self.ListingDate = IPOInfoList[4]
        # self.GlobalOfferedShares = IPOInfoList[5]
        # self.HKOfferedShares = IPOInfoList[6]
        # self.InternationalShares = IPOInfoList[7]
        # self.Underwriter = IPOInfoList[8]
        # self.Sponsors = IPOInfoList[9]

    def addFinancialComp(self, financialCompList, labels):
        for i,label in enumerate(labels):
            if label not in self.financialComp:
                self.financialComp[label] = financialCompList[i]

    def printFinancialComp(self):
        for k,v in self.financialComp.items():
            print(k, "\t\t\t", v)

    def printIPOInfo(self):
        for k,v in self.info.items():
            print(k, "\t\t\t", v)

    def addPnL(self, PnLList, labels):
        for i,label in enumerate(labels):
            if label not in self.PnL:
                self.PnL[label] = PnLList[i]

    def printPnL(self):
        for k,v in self.PnL.items():
            print(k, "\t\t\t", v)

    def getLabels(self):
        label = []
        label.append("Name")
        label.append("ID")
        for k in self.info.keys():
            label.append(k)
        for k in self.financialComp.keys():
            label.append(k)
        for k in self.PnL.keys():
            label.append(k)
        return label

    def getValues(self):
        """
        pass
        :return: all attributes as list
        """
        values = []
        values.append(self.name)
        values.append(self.id)
        for v in self.info.values():
            values.append(v)
        for v in self.financialComp.values():
            values.append(v)
        for v in self.PnL.values():
            values.append(v)
        return values

    def formatAttributes(self):
        # Offer price split into upper and lower
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

        #book value, just delete atm
        self.info.pop('Book Value')

        #Market Cap
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

        # No. of Global Offered Shares2
        num = self.info["No. of Global Offered Shares2"]
        if num != "N/A":
            self.info["No. of Global Offered Shares2"] = float(num.replace(",",""))
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

        #start dealing with multiyear shit

    # def writeToWeka(self, output_filename):
    #
    #     with open(output_filename, 'w', encoding='utf-8', newline="") as arffFile:
    #         arffFile.write('''@RELATION IPO\n''')
