import argparse
import sys
sys.path.append("scripts")
 
from extract import extract
from transform import transform
from load_staging import load_staging
from validate import run_validations
from load_production import (
    get_conn, load_dim_carrier, load_dim_airport,
    load_dim_date, load_fact_flights
)
 
def main(run_date):
    print(f"Starting pipeline run for {run_date}")
 
    df = extract()
    df = transform(df)
 
    if run_date:
        df = df[df["FL_DATE"].dt.strftime("%Y-%m-%d") == run_date]
        print(f"Filtered to {len(df)} rows for {run_date}")
 
    load_staging(df)
    run_validations(df)
 
    conn = get_conn()
    cursor = conn.cursor()
    load_dim_carrier(cursor, df)
    load_dim_airport(cursor, df)
    load_dim_date(cursor, df)
    conn.commit()
    load_fact_flights(cursor, df)
    conn.commit()
    cursor.close()
    conn.close()
 
    print("Pipeline run complete.")
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="YYYY-MM-DD, process only this day", default=None)
    args = parser.parse_args()
    main(args.date)