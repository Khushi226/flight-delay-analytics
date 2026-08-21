import mysql.connector
import pandas as pd
 
def load_staging(df):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",   # the one you set in Part 0.3
        database="flight_analytics",
    )
    cursor = conn.cursor()
 
    insert_query = """
        INSERT INTO staging_flights (
            fl_date, carrier, tail_num, flight_num, origin, origin_city,
            dest, dest_city, crs_dep_time, dep_time, dep_delay,
            crs_arr_time, arr_time, arr_delay, cancelled, diverted,
            carrier_delay, weather_delay, nas_delay, security_delay,
            late_aircraft_delay, missing_tail_num
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
 
    cols = [
        "FL_DATE","OP_UNIQUE_CARRIER","TAIL_NUM","OP_CARRIER_FL_NUM",
        "ORIGIN","ORIGIN_CITY_NAME","DEST","DEST_CITY_NAME",
        "CRS_DEP_TIME","DEP_TIME","DEP_DELAY","CRS_ARR_TIME","ARR_TIME",
        "ARR_DELAY","CANCELLED","DIVERTED","CARRIER_DELAY","WEATHER_DELAY",
        "NAS_DELAY","SECURITY_DELAY","LATE_AIRCRAFT_DELAY","MISSING_TAIL_NUM",
    ]
 
    data = df[cols].astype(object).where(pd.notnull(df[cols]), None).values.tolist()
 
    # executemany + batching -- inserting 544,000 rows one at a time
    # would take forever, so we send them in chunks of 5,000
    batch_size = 5000
    for i in range(0, len(data), batch_size):
        cursor.executemany(insert_query, data[i:i + batch_size])
        conn.commit()
        print(f"Inserted rows {i} to {i + batch_size}")
 
    cursor.close()
    conn.close()