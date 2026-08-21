import pandas as pd
 
def transform(df):
    # 1. Fix FL_DATE: it's a text string like "1/1/2026 12:00:00 AM"
    #    with a format pandas can't auto-detect reliably at this size,
    #    so we give it the exact format explicitly.
    df["FL_DATE"] = pd.to_datetime(
        df["FL_DATE"], format="%m/%d/%Y %I:%M:%S %p"
    )
 
    # 2. Standardize CANCELLED / DIVERTED to real booleans (0/1 -> True/False)
    df["CANCELLED"] = df["CANCELLED"].astype(bool)
    df["DIVERTED"]  = df["DIVERTED"].astype(bool)
 
    # 3. Delay columns should be null ONLY for cancelled flights.
    #    For flights that flew but weren't delayed, missing delay-cause
    #    values really mean 0 minutes -- fill them with 0, but only
    #    for flights that actually departed.
    delay_cause_cols = [
        "CARRIER_DELAY", "WEATHER_DELAY", "NAS_DELAY",
        "SECURITY_DELAY", "LATE_AIRCRAFT_DELAY",
    ]
    flew_mask = df["CANCELLED"] == False
    for col in delay_cause_cols:
        df.loc[flew_mask, col] = df.loc[flew_mask, col].fillna(0)
 
    # 4. Flag rows with a genuinely missing TAIL_NUM (real data gap)
    df["MISSING_TAIL_NUM"] = df["TAIL_NUM"].isnull()
 
    # 5. Drop exact duplicate rows, if any (defensive -- there were
    #    none in this file, but a real pipeline must always check)
    before = len(df)
    df = df.drop_duplicates()
    print(f"Removed {before - len(df)} duplicate rows")
 
    return df