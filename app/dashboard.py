from pathlib import Path
import pandas as pd
import streamlit as st
ROOT=Path(__file__).parents[1]; R=ROOT/'results'
st.set_page_config(page_title='Commerce Intelligence',layout='wide')
st.title('Commerce Intelligence Dashboard'); st.caption('Revenue, profitability, retention and customer priorities')
k=pd.read_csv(R/'kpis.csv').iloc[0]; c=st.columns(4); c[0].metric('Revenue',f"${k.revenue:,.0f}"); c[1].metric('Gross profit',f"${k.gross_profit:,.0f}"); c[2].metric('Margin',f"{k.margin_pct:.1%}"); c[3].metric('Repeat customers',f"{k.repeat_customer_rate:.1%}")
monthly=pd.read_csv(R/'monthly.csv'); st.subheader('Monthly performance'); st.line_chart(monthly.set_index('month')[['revenue','gross_profit']])
left,right=st.columns(2); left.subheader('Customer segments'); left.dataframe(pd.read_csv(R/'rfm.csv').groupby('segment').agg(customers=('customer_id','count'),revenue=('monetary','sum'),risk=('risk_score','mean')).reset_index(),use_container_width=True); right.subheader('Revenue forecast'); right.dataframe(pd.read_csv(R/'forecast.csv'),use_container_width=True)
st.subheader('Product profitability'); st.dataframe(pd.read_csv(R/'product_analysis.csv').head(20),use_container_width=True)
