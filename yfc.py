import yfinance as yf 

class Yfc():
 
    def __init__(self):
        pass

    def getInfo(self, sym):
        ticker = yf.Ticker(sym)
        return ticker