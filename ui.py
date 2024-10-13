import streamlit as st
from yfc import Yfc
from loguru import logger 

st.title("Yahoo Stocks Dashboard")


sym = st.text_input("Enter stock", "0005.HK")
yfc = Yfc()
symInfo=yfc.getInfo(sym)
# (net profit * 1.022)/0.07/diluted shares
netprofit=symInfo.income_stmt.loc['Net Income']
dilutedshares=symInfo.income_stmt.loc['Diluted Average Shares']
st.write("Fair value based on prev net income")
st.write(netprofit.iloc[0] * 1.04 / 0.07/dilutedshares.iloc[0])

st.write("Dividends", symInfo.dividends)
#for key in symInfo.basic_info:
#    st.write(key,symInfo.basic_info[key])

#for key in symInfo.income_stmt.keys():
#    st.write(key, symInfo.income_stmt[key]['Net Income'])
#logger.info(f'{symInfo.income_stmt.keys()}')
#st.dataframe(symInfo.income_stmt.get('2023-12-31 00:00:00'))
st.write("Earnings", symInfo.income_stmt)
