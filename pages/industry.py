import streamlit as st
from menu import menu
from yfc import Yfc

if 'industry' not in st.session_state:
    st.session_state['industry'] = 'banks-diversified'
    
menu()

yfc = Yfc()
industryInfo=yfc.getIndustry(st.session_state['industry'])
st.title("Industry Analytics")
st.write(f'{st.session_state['industry']}')
st.write("Top Performing Companies", industryInfo.top_performing_companies)