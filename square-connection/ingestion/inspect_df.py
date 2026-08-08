import pandas as pd

df = pd.read_parquet('../data/TestBusinessAcc/sales_raw.parquet')
print(df.shape)          # (rows, cols)
print(df.dtypes)         # col names + types
print(df.head(2))        # first 2 rows
print(df.isnull().sum()) # null counts per column