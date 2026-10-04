from __future__ import annotations
import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def kpis(df):
    d = df[df.is_completed]
    customers = d.customer_id.nunique()
    orders = d.order_id.nunique()
    revenue = d.net_revenue.sum()
    profit = d.gross_profit.sum()
    return pd.DataFrame([{'orders':orders,'customers':customers,'revenue':revenue,'gross_profit':profit,'margin_pct':profit/revenue if revenue else 0,'avg_order_value':revenue/orders if orders else 0,'repeat_customer_rate': repeat_rate(d)}])

def repeat_rate(d):
    counts = d.groupby('customer_id')['order_id'].nunique()
    return (counts.gt(1).mean() if len(counts) else 0)

def monthly(d):
    x = d[d.is_completed].groupby('month', as_index=False).agg(revenue=('net_revenue','sum'),gross_profit=('gross_profit','sum'),orders=('order_id','nunique'),customers=('customer_id','nunique'),discounts=('discount_value','sum'))
    x['margin_pct'] = x.gross_profit / x.revenue.replace(0,np.nan)
    x['aov'] = x.revenue / x.orders.replace(0,np.nan)
    return x

def cohort_retention(d):
    d=d[d.is_completed].copy(); d['order_month']=d.order_date.dt.to_period('M').dt.to_timestamp(); first=d.groupby('customer_id').order_month.min().rename('cohort_month'); d=d.join(first,on='customer_id'); d['period']=(d.order_month.dt.year-d.cohort_month.dt.year)*12+d.order_month.dt.month-d.cohort_month.dt.month
    out=d.groupby(['cohort_month','period']).customer_id.nunique().reset_index(); base=out[out.period.eq(0)].set_index('cohort_month').customer_id.rename('cohort_size'); out=out.join(base,on='cohort_month'); out['retention']=out.customer_id/out.cohort_size; return out

def rfm(d, as_of=None):
    d=d[d.is_completed].copy(); as_of=as_of or (d.order_date.max()+pd.Timedelta(days=1)); x=d.groupby('customer_id').agg(last_order=('order_date','max'),frequency=('order_id','nunique'),monetary=('net_revenue','sum')).reset_index(); x['recency']=(as_of-x.last_order).dt.days; x['r_score']=pd.qcut(x.recency.rank(method='first'),5,labels=[5,4,3,2,1]).astype(int); x['f_score']=pd.qcut(x.frequency.rank(method='first'),5,labels=[1,2,3,4,5]).astype(int); x['m_score']=pd.qcut(x.monetary.rank(method='first'),5,labels=[1,2,3,4,5]).astype(int); x['rfm_score']=x.r_score+x.f_score+x.m_score; x['segment']=np.select([x.rfm_score>=13,x.rfm_score>=10,x.recency>90],["Champions","Loyal","At risk"],default='Potential'); x['risk_score']=(x.recency/x.recency.median()*0.6 + 1/(x.frequency)*0.2 + 1/(x.monetary/x.monetary.median())*0.2).clip(0,10); return x

def product_analysis(d):
    return d[d.is_completed].groupby(['category','product'],as_index=False).agg(revenue=('net_revenue','sum'),profit=('gross_profit','sum'),units=('quantity','sum'),orders=('order_id','nunique'),avg_discount=('discount_pct','mean')).assign(margin_pct=lambda x:x.profit/x.revenue.replace(0,np.nan)).sort_values('profit',ascending=False)

def forecast(monthly_df, horizon=3):
    y=monthly_df.set_index(pd.to_datetime(monthly_df.month+'-01')).revenue.asfreq('MS').fillna(0)
    model=ExponentialSmoothing(y, trend='add', damped_trend=True).fit(optimized=True)
    pred=model.forecast(horizon); return pd.DataFrame({'month':pred.index.strftime('%Y-%m'),'forecast_revenue':pred.values})
