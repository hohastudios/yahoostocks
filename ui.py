import streamlit as st
from yfc import Yfc
from loguru import logger 
import math

st.title("Yahoo Stocks Dashboard")


sym = st.text_input("Enter stock", "0005.HK")
y30yield=float(st.text_input("30Y yields %", 4) ) / 100 +1
targetgrowth=float(st.text_input("Custom target growth %", 0)) / 100 + 1
yfc = Yfc()
symInfo=yfc.getInfo(sym)
# (net profit * 1.022)/0.07/diluted shares
netprofitfull=symInfo.income_stmt.loc['Net Income']
if math.isnan(netprofitfull.iloc[0]):
    netprofit=netprofitfull.iloc[1]
else:
    netprofit=netprofitfull.iloc[0]

dilutedsharesfull=symInfo.income_stmt.loc['Diluted Average Shares']

if math.isnan(dilutedsharesfull.iloc[0]):
    dilutedshares=dilutedsharesfull.iloc[1]
else:
    dilutedshares=dilutedsharesfull.iloc[0]

st.write("Fair value based on prev net income and GG model")
st.write("Conservative lower band ", f"{netprofit}", " ")
st.write(netprofit * targetgrowth * y30yield / 0.07 / dilutedshares)
st.write("Aggressive upper band")
st.write(netprofit * targetgrowth * y30yield / 0.05 / dilutedshares)

st.write("Dividends", symInfo.dividends)

st.write("Earnings", symInfo.income_stmt)

st.write("Quaterly Earnings", symInfo.quarterly_financials)

st.write("Analyst Targets", symInfo.analyst_price_targets)

st.write("Earning Estimates", symInfo.earnings_estimate)

st.write("Earnings Dates", symInfo.earnings_dates)


st.write("Disclaimer: This site is purely for personal and educational use \
    Yahoo!, Y!Finance, and Yahoo! finance are registered trademarks of Yahoo, Inc. \
    This site is not affilited, endorsed or vetted by Yahoo, Inc.\
    API is yfinance, and is not affiliated, endorsed, or vetted by Yahoo, Inc.\
    It's an open-source tool that uses Yahoo's publicly available APIs, and is intended for research and educational purposes. \
    You should refer to Yahoo!'s terms of use (here, here, and here) for details on your rights to use the actual data downloaded. \
    Remember - the Yahoo! finance API is intended for personal use only.\
    ")