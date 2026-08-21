import mysql.connector
import pandas as pd

import math

def nan_to_none(val):
    # NaN only exists for floats -- this safely converts it to None,
    # leaves every other value (including 0, False, valid numbers) untouched
    if isinstance(val, float) and math.isnan(val):
        return None
    return val
 
def get_conn():
    return mysql.connector.connect(
        host="localhost", user="root",
        password="1234", database="flight_analytics",
    )
 
def load_dim_carrier(cursor, df):
    carriers = df["OP_UNIQUE_CARRIER"].dropna().unique()
    for c in carriers:
        cursor.execute(
            "INSERT IGNORE INTO Dim_Carrier (carrier_code) VALUES (%s)", (c,)
        )
 
def load_dim_airport(cursor, df):
    airports = pd.concat([
        df[["ORIGIN", "ORIGIN_CITY_NAME"]].rename(
            columns={"ORIGIN": "code", "ORIGIN_CITY_NAME": "city"}),
        df[["DEST", "DEST_CITY_NAME"]].rename(
            columns={"DEST": "code", "DEST_CITY_NAME": "city"}),
    ]).drop_duplicates(subset="code")
    for _, row in airports.iterrows():
        cursor.execute(
            "INSERT IGNORE INTO Dim_Airport (airport_code, city_name) VALUES (%s,%s)",
            (row["code"], row["city"]),
        )
 
def load_dim_date(cursor, df):
    dates = df["FL_DATE"].dropna().dt.date.unique()
    for d in dates:
        cursor.execute(
            "INSERT IGNORE INTO Dim_Date (full_date, day_of_week, day_of_month, "
            "month, is_weekend) VALUES (%s,%s,%s,%s,%s)",
            (d, d.strftime("%A"), d.day, d.month, d.weekday() >= 5),
        )
 
def load_fact_flights(cursor, df):
    # build lookup maps: code -> generated ID, so we can translate
    # each raw row into the correct foreign keys
    cursor.execute("SELECT carrier_id, carrier_code FROM Dim_Carrier")
    carrier_map = {code: cid for cid, code in cursor.fetchall()}
 
    cursor.execute("SELECT airport_id, airport_code FROM Dim_Airport")
    airport_map = {code: aid for aid, code in cursor.fetchall()}
 
    cursor.execute("SELECT date_id, full_date FROM Dim_Date")
    date_map = {d: did for did, d in cursor.fetchall()}
 
    insert_query = """
        INSERT INTO Fact_Flights (
            date_id, carrier_id, origin_airport_id, dest_airport_id,
            dep_delay, arr_delay, cancelled, diverted, carrier_delay,
            weather_delay, nas_delay, security_delay, late_aircraft_delay
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    rows = []
    for _, r in df.iterrows():
        rows.append((
    date_map.get(r["FL_DATE"].date()),
    carrier_map.get(r["OP_UNIQUE_CARRIER"]),
    airport_map.get(r["ORIGIN"]),
    airport_map.get(r["DEST"]),
    nan_to_none(r["DEP_DELAY"]), nan_to_none(r["ARR_DELAY"]), bool(r["CANCELLED"]),
    bool(r["DIVERTED"]), nan_to_none(r["CARRIER_DELAY"]), nan_to_none(r["WEATHER_DELAY"]),
    nan_to_none(r["NAS_DELAY"]), nan_to_none(r["SECURITY_DELAY"]), nan_to_none(r["LATE_AIRCRAFT_DELAY"]),
))
 
    batch = 5000
    for i in range(0, len(rows), batch):
        cursor.executemany(insert_query, rows[i:i + batch])
        print(f"Fact rows loaded: {i + batch}")