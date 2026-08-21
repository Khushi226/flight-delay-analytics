import mysql.connector
 
def log_issue(cursor, check_name, description, row_count):
    cursor.execute(
        "INSERT INTO data_quality_logs (check_name, issue_description, row_count) "
        "VALUES (%s, %s, %s)",
        (check_name, description, row_count),
    )
 
def run_validations(df):
    conn = mysql.connector.connect(
        host="localhost", user="root",
        password="1234", database="flight_analytics",
    )
    cursor = conn.cursor()
 
    # Check 1: completeness -- flag genuinely missing tail numbers
    missing_tail = df["MISSING_TAIL_NUM"].sum()
    if missing_tail > 0:
        log_issue(cursor, "completeness_tail_num",
                   "Flights with missing aircraft tail number", int(missing_tail))
 
    # Check 2: referential sanity -- a flight can't be both
    # cancelled AND have recorded arrival delay minutes
    bad_cancel = df[(df["CANCELLED"] == True) & (df["ARR_DELAY"].notnull())]
    if len(bad_cancel) > 0:
        log_issue(cursor, "logical_consistency_cancelled",
                   "Cancelled flights with a non-null arrival delay", len(bad_cancel))
 
    # Check 3: validity -- delay minutes should never be negative
    #  beyond a reasonable early-arrival bound (sanity threshold)
    extreme_early = df[df["ARR_DELAY"] < -60]
    if len(extreme_early) > 0:
        log_issue(cursor, "validity_extreme_early_arrival",
                   "Flights arriving more than 60 min early (possible bad data)",
                   len(extreme_early))
 
    # Check 4: uniqueness -- duplicate flight numbers on the exact
    # same date + carrier (excluding legitimate multi-leg same-day flights
    # is out of scope here, so we flag for manual review instead of dropping)
    dupes = df.duplicated(subset=["FL_DATE", "OP_UNIQUE_CARRIER", "OP_CARRIER_FL_NUM"])
    if dupes.sum() > 0:
        log_issue(cursor, "uniqueness_flight_number",
                   "Duplicate carrier+flight number on the same date", int(dupes.sum()))
 
    conn.commit()
    cursor.close()
    conn.close()
    print("Validation complete -- see data_quality_logs table")