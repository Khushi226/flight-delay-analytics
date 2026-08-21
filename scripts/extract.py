import pandas as pd

RAW_PATH="data/raw/T_ONTIME_REPORTING.csv"

def extract():
    df=pd.read_csv(RAW_PATH, low_memory=False)
    print(f"Loaded {len(df):,} rows and {len(df.columns)} columns")
    print(df.head())
    print(df.isnull().sum())
    return df

if __name__=="__main__":
    extract()
