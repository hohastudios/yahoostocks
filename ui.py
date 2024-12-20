import streamlit as st
from yfc import Yfc
from loguru import logger 
import math
from menu import menu
import numpy as np
import pandas as pd
import json

def storeSymbol(sym):
    st.session_state['symbol_input'] = sym

def storeIndustry(industry):
    st.session_state['industry']=industry

menu()

#Initialize sessions variables 

if ('symbol' not in st.session_state and 'state' not in st.session_state):
    st.session_state['symbol'] = '0005.HK'
    st.session_state['state'] = 'first_initialised'

if 'industry' not in st.session_state:
    st.session_state['industry'] = 'banks-diversified'

st.title("Yahoo Stocks Dashboard")

st.write("Disclaimer: This site is purely for personal and educational use \
    Yahoo!, Y!Finance, and Yahoo! finance are registered trademarks of Yahoo, Inc. \
    This site is not affilited, endorsed or vetted by Yahoo, Inc.\
    API is yfinance, and is not affiliated, endorsed, or vetted by Yahoo, Inc.\
    It's an open-source tool that uses Yahoo's publicly available APIs, and is intended for research and educational purposes. \
    You should refer to Yahoo!'s terms of use (here, here, and here) for details on your rights to use the actual data downloaded. \
    Remember - the Yahoo! finance API is intended for personal use only.\
    ")


if st.session_state['state'] == 'first_initialised':
    sym = st.text_input("Enter stock", st.session_state.symbol, key='symbol_input')
else:
    if 'symbol_input' not in st.session_state:
        st.session_state['symbol_input'] = '0005.HK'
    sym = st.text_input("Enter stock", st.session_state.symbol_input, key='symbol_input')


st.session_state['state']="refreshed"


y30yield=float(st.text_input("30Y yields %", 4) ) / 100 +1
targetgrowth=float(st.text_input("Custom target growth %", 0)) / 100 + 1

yfc = Yfc()
symInfo=yfc.getInfo(sym)

if 'debtToEquity' in symInfo.get_info().keys():
    debtToEquityVal=100-(symInfo.get_info()['debtToEquity'])
  
else:
    debtToEquityVal=100

debtToEquity=float(st.text_input("Propotion in Equity", debtToEquityVal)) / 100
if 'industryKey' in symInfo.get_info().keys():
    storeIndustry(symInfo.get_info()['industryKey'])
    
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

exchangeCurrency=symInfo.get_info()['currency']
reportingCurrency=symInfo.get_info()['financialCurrency']

exRate = 1.0
if (exchangeCurrency != reportingCurrency):
    yfcFx = Yfc()
    currInfo=yfcFx.getInfo(reportingCurrency+exchangeCurrency+"=X")
    exRate = currInfo.get_info()["previousClose"]

st.write("Fair value based on prev net income and GG model")
st.write("Net Profit from Income Statement: " ,f"{netprofit:,.0f}", " ", f"{exchangeCurrency}")

d = {'Conservative lower band' : [f"{netprofit * exRate * targetgrowth * y30yield * debtToEquity / 0.07 / dilutedshares:,.2f} {exchangeCurrency}"],
     'Aggressive upper band' : [f"{netprofit * exRate * targetgrowth * y30yield * debtToEquity  / 0.05 / dilutedshares:,.2f} {exchangeCurrency}"]}

df=pd.DataFrame(data=d)
st.write(df)

st.write("Analyst Targets", symInfo.analyst_price_targets)

st.write("Dividends", symInfo.dividends[::-1])

earnings_container_yearly = st.container()
with earnings_container_yearly:
    earnings_yearly, earnings_yearly_pct_change = st.columns(2)
    with earnings_yearly:
        st.write("Yearly Earnings") 
        st.dataframe(symInfo.get_financials(freq="yearly").loc['NetIncome'],use_container_width=True)
    with earnings_yearly_pct_change:
        d=symInfo.get_financials(freq="yearly").loc['NetIncome'][::-1]
        df=pd.DataFrame(data=d)
        s= (df['NetIncome'].shift(-1) - df['NetIncome']).abs() / np.abs(df['NetIncome']) * 100
        st.write("Yearly Earnings (% Chg)")
        st.dataframe(s.shift(1)[::-1],use_container_width=True)
        #st.write("Yearly Earnings (% Chg)", (symInfo.get_financials(freq="yearly").loc['NetIncome'][::-1].pct_change()*100)[::-1])

try:
    earnings_container_quarterly = st.container()
    with earnings_container_quarterly:
        earnings_quarterly, earnings_quarterly_pct_change = st.columns(2)
        with earnings_quarterly:
            st.write("Quarterly Earnings")
            st.dataframe(symInfo.get_financials(freq="quarterly").loc['NetIncome'], use_container_width=True)
        with earnings_quarterly_pct_change:
            d=symInfo.get_financials(freq="quarterly").loc['NetIncome'][::-1]
            df=pd.DataFrame(data=d)
            s= (df['NetIncome'].shift(-1, fill_value=0) - df['NetIncome']).abs() / np.abs(df['NetIncome']) * 100
            st.write("Quarterly Earnings (% Chg)")
            st.dataframe(s.shift(1)[::-1],use_container_width=True)
except Exception:
    pass
    
with st.expander("See Breakdown"):
    st.write("Earnings", symInfo.income_stmt)
    st.write("Quarterly Earnings", symInfo.quarterly_financials)
    st.write("Balance Sheet", symInfo.balance_sheet)

try:
    st.write("Growth Estimates", symInfo.get_growth_estimates())
except Exception:
    pass

try:
    st.write("Earning Estimates", symInfo.earnings_estimate)
except Exception:
    pass


#st.write("Earnings Dates", symInfo.earnings_dates)
st.write("Recommendations", symInfo.recommendations_summary)
with st.expander("See Calender"):
    st.write(symInfo.get_calendar())
st.write("Institutional Holders", symInfo.get_major_holders())

with st.expander("See Fast Info"):
    for key in symInfo.fast_info:
        st.write(f"{key}" , " : ", symInfo.fast_info[key])

with st.expander("See Full Info"):
    st.write("Full Info", symInfo.get_info())

st.write("Disclaimer: This site is purely for personal and educational use \
    Yahoo!, Y!Finance, and Yahoo! finance are registered trademarks of Yahoo, Inc. \
    This site is not affilited, endorsed or vetted by Yahoo, Inc.\
    API is yfinance, and is not affiliated, endorsed, or vetted by Yahoo, Inc.\
    It's an open-source tool that uses Yahoo's publicly available APIs, and is intended for research and educational purposes. \
    You should refer to Yahoo!'s terms of use (here, here, and here) for details on your rights to use the actual data downloaded. \
    Remember - the Yahoo! finance API is intended for personal use only.\
    ")
