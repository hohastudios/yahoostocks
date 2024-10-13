import streamlit as st
from yfc import Yfc
from loguru import logger 
import math

st.title("Yahoo Stocks Dashboard")


sym = st.text_input("Enter stock", "0005.HK")
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


st.write("Fair value based on prev net income")
st.write(netprofit* 1.04 / 0.07/dilutedshares)

st.write("Dividends", symInfo.dividends)
#for key in symInfo.basic_info:
#    st.write(key,symInfo.basic_info[key])

#for key in symInfo.income_stmt.keys():
#    st.write(key, symInfo.income_stmt[key]['Net Income'])
#logger.info(f'{symInfo.income_stmt.keys()}')
#st.dataframe(symInfo.income_stmt.get('2023-12-31 00:00:00'))
st.write("Earnings", symInfo.income_stmt)

st.write("Disclaimer: This site is purely for personal and educational use \
    Yahoo!, Y!Finance, and Yahoo! finance are registered trademarks of Yahoo, Inc. \
    This site is not affilited, endorsed or vetted by Yahoo, Inc.\
    API is yfinance, and is not affiliated, endorsed, or vetted by Yahoo, Inc.\
    It's an open-source tool that uses Yahoo's publicly available APIs, and is intended for research and educational purposes. \
    You should refer to Yahoo!'s terms of use (here, here, and here) for details on your rights to use the actual data downloaded. \
    Remember - the Yahoo! finance API is intended for personal use only.\
    ")