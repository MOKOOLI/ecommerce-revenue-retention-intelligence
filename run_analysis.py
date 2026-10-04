from pathlib import Path
import pandas as pd
from src.cleaning import load_and_clean
from src.metrics import kpis,monthly,cohort_retention,rfm,product_analysis,forecast
from src.visuals import save_all
ROOT=Path(__file__).parent

def main():
    df=load_and_clean(ROOT/'data/raw/orders.csv'); d=df[df.is_completed].copy(); out=ROOT/'results'; out.mkdir(exist_ok=True)
    tables={'kpis':kpis(df),'monthly':monthly(df),'cohort_retention':cohort_retention(d),'rfm':rfm(d),'product_analysis':product_analysis(df),'forecast':forecast(monthly(df))}
    for name,t in tables.items(): t.to_csv(out/f'{name}.csv',index=False)
    save_all(df,tables['monthly'],tables['cohort_retention'],tables['rfm'],tables['product_analysis'])
    memo=f'''# Commercial recommendations\n\n1. Protect the highest-profit product and channel combinations before increasing volume.\n2. Build a win-back campaign for the At risk segment, prioritising customers with high monetary value.\n3. Review categories with high average discount and below-average margin.\n4. Use the cohort table to track whether new-customer retention improves month over month.\n5. Treat the forecast as a planning baseline, not a promise; refresh it after each completed month.\n'''
    (out/'recommendations.md').write_text(memo)
    print('Completed:',len(df),'rows;',len(d.customer_id.unique()),'customers')
if __name__=='__main__': main()
