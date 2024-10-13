import streamlit as st
from yfc import Yfc
from loguru import logger 

st.title("Yahoo Stocks Dashboard")


sym = st.text_input("Enter stock", "0005.HK")
yfc = Yfc()
symInfo=yfc.getInfo(sym)

st.write("Dividends", symInfo.dividends)
#for key in symInfo.basic_info:
#    st.write(key,symInfo.basic_info[key])

st.write("Net Profit")
#for key in symInfo.income_stmt.keys():
#    st.write(key, symInfo.income_stmt[key]['Net Income'])
#logger.info(f'{symInfo.income_stmt.keys()}')
#st.dataframe(symInfo.income_stmt.get('2023-12-31 00:00:00'))
st.write("Earnings", symInfo.income_stmt)
