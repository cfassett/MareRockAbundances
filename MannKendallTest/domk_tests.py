import pymannkendall as mk
import pandas as pd


df=pd.read_csv('5.csv')
result=mk.original_test(df)
print("5: ")
print(result)

df=pd.read_csv('med.csv')
result=mk.original_test(df)
print("med: ")
print(result)

df=pd.read_csv('95.csv')
result=mk.original_test(df)
print("95: ")
print(result)

df=pd.read_csv('binnedmean.csv')
result=mk.original_test(df)
print("avg: ")
print(result)

import pymannkendall as mk
import pandas as pd


df=pd.read_csv('allrawdata_ex.csv')
sv=df.sort_values(by=['freq'])
raseries=pd.to_numeric(sv['ra'],downcast='float')

rasample=raseries[::1000]
result=mk.original_test(rasample)
print("sample every 1000:")
print(result)
