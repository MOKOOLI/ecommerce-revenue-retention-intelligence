from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def save_all(df, monthly, cohort, rfm, products, out='figures'):
    Path(out).mkdir(exist_ok=True); sns.set_theme(style='whitegrid')
    p=pd.to_datetime(monthly.month+'-01'); fig,ax=plt.subplots(figsize=(10,5)); ax.plot(p,monthly.revenue,marker='o',label='Revenue'); ax.plot(p,monthly.gross_profit,marker='o',label='Gross profit'); ax.set_title('Revenue and gross profit trend'); ax.legend(); fig.tight_layout(); fig.savefig(f'{out}/01_revenue_profit.png',dpi=160); plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,5)); piv=cohort.pivot(index='cohort_month',columns='period',values='retention'); sns.heatmap(piv,annot=True,fmt='.0%',cmap='Blues',vmin=0,vmax=1,ax=ax); ax.set_title('Customer cohort retention'); fig.tight_layout(); fig.savefig(f'{out}/02_cohort_retention.png',dpi=160); plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5)); top=products.head(12).sort_values('profit'); ax.barh(top['product'],top['profit'],color='#2364aa'); ax.set_title('Top products by gross profit'); fig.tight_layout(); fig.savefig(f'{out}/03_product_profit.png',dpi=160); plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,5)); sns.scatterplot(data=rfm,x='recency',y='monetary',size='frequency',hue='segment',alpha=.75,ax=ax); ax.set_title('Customer value and inactivity'); fig.tight_layout(); fig.savefig(f'{out}/04_customer_segments.png',dpi=160); plt.close(fig)
