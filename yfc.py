import yfinance as yf 

class Yfc():
 
    def __init__(self):
        pass

    def getInfo(self, sym):
        return yf.Ticker(sym)
    
    def getIndustry(self, industry):
        return yf.Industry(industry)
    
    def getSector(self, sector):
        return yf.Sector(sector)