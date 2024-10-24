import tushare as ts
import sys

    
ts.set_token('23fb254f8a8c74cdebf7406ed95985090e1422f5705629455367b09b')
pro = ts.pro_api()
df = pro.weekly(ts_code='000001.SZ', start_date='20241008', end_date='20241024', fields='ts_code,trade_date,open,high,low,close,vol,amount')
print(df)