from src.cleaning import load_and_clean
from src.metrics import kpis,monthly,cohort_retention,rfm

def test_pipeline_outputs():
 d=load_and_clean('data/raw/orders.csv'); assert len(d)>0; assert d.net_revenue.notna().all(); assert kpis(d).iloc[0].revenue>0; assert len(monthly(d))>3; assert len(cohort_retention(d[d.is_completed]))>0; assert len(rfm(d[d.is_completed]))>0
