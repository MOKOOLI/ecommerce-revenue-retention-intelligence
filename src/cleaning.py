from __future__ import annotations
import pandas as pd
import numpy as np

REQUIRED = ['order_id','order_date','customer_id','product','category','channel','region','quantity','unit_price','unit_cost','discount_pct','status']

def load_and_clean(path):
    raw = pd.read_csv(path)
    missing = sorted(set(REQUIRED) - set(raw.columns))
    if missing: raise ValueError(f'Missing columns: {missing}')
    df = raw.copy()
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce', utc=True).dt.tz_convert(None)
    for c in ['quantity','unit_price','unit_cost','discount_pct']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df['category'] = df['category'].astype('string').str.strip().str.lower().replace({'home & garden':'home','home and garden':'home','elec.':'electronics'})
    df['channel'] = df['channel'].astype('string').str.strip().str.lower()
    df['region'] = df['region'].astype('string').str.strip().str.title()
    df['status'] = df['status'].astype('string').str.strip().str.lower()
    df['discount_pct'] = df['discount_pct'].clip(0, 0.95)
    df['quantity'] = df['quantity'].clip(lower=1)
    df['order_date'] = df['order_date'].fillna(df['order_date'].median())
    df['customer_id'] = df['customer_id'].fillna('UNKNOWN')
    df['is_completed'] = df['status'].eq('completed')
    df['is_refund'] = df['status'].eq('refunded')
    df['is_cancelled'] = df['status'].eq('cancelled')
    sign = np.where(df['is_refund'], -1, 1)
    df['gross_sales'] = df['quantity'] * df['unit_price'] * sign
    df['discount_value'] = df['gross_sales'].abs() * df['discount_pct']
    df['net_revenue'] = df['gross_sales'] * (1 - df['discount_pct'])
    df['cost'] = df['quantity'] * df['unit_cost'] * sign
    df['gross_profit'] = df['net_revenue'] - df['cost']
    df['margin_pct'] = np.where(df['net_revenue'] != 0, df['gross_profit'] / df['net_revenue'], 0)
    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    df = df.drop_duplicates(subset=['order_id'], keep='first')
    return df

def completed(df):
    return df[df['is_completed'] & (df['customer_id'] != 'UNKNOWN')].copy()
