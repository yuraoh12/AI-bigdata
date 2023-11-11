import streamlit as st
import pandas_datareader as pdr
import datetime
import yfinance as yf
yf.pdr_override()

st.write('''
# 삼성전자 주식 데이터
마감 가격과 거래량을 차트로 보여줍니다!
''')
start_time = datetime.datetime(2020, 1, 1)
end_time = datetime.datetime(2020, 9, 30)

# https://finance.yahoo.com/quote/005930.KS?p=005930.KS
df = pdr.get_data_yahoo('005930.KS', start_time, end_time) # 005930.KS '2020-01-01' 2020-09-30
pdr.get_data_yahoo()
st.line_chart(df.Volume)