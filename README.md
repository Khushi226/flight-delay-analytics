
# ✈️ Flight Delay Analytics Pipeline

An end-to-end data engineering pipeline that ingests raw U.S. Bureau of Transportation Statistics (BTS) flight records, validates data integrity through a custom Data Quality framework, models data into a MySQL star schema, and delivers operational delay insights via a live Power BI dashboard.

---

## 📌 Project Overview
This project simulates an enterprise-grade data warehouse ingestion pipeline. Raw aviation data containing hundreds of thousands of flight records is extracted, transformed, and validated to uncover flight delay patterns, cancellation drivers, and airline performance metrics. The pipeline enforces strict data governance and auditing at every stage of the ETL process.

---

## 🏗️ Architecture & Data Flow

```text
[ Raw BTS CSV ] 
       │
       ▼
EXTRACT ─────────> Load raw flight records into Python (Pandas)
       │
       ▼
TRANSFORM ───────> Standardize dates/times, deduplicate, process cancellation logic
       │
       ▼
STAGING ─────────> Push transformed data into MySQL staging tables (stg_flights)
       │
       ▼
VALIDATE ────────> Run quality checks (completeness, uniqueness, referential integrity);
                   Log anomalies to audit_logs table
       │
       ▼
PRODUCTION ──────> Promote passed records to Star Schema (Fact_Flights, Dim_Airport, Dim_Airline)
       │
       ▼
REPORT ──────────> Power BI dashboard connected live to MySQL production schema


🛠️ Tech Stack
1.Language & Data Processing: Python (pandas, sqlalchemy, datetime)

2.Database & Data Warehouse: MySQL (Staging Layer, Audit System, Star Schema Production Warehouse)

3.Business Intelligence: Power BI (Direct / Live Database Querying)

4.Data Source: U.S. Department of Transportation (BTS Reporting Carrier On-Time Performance)

⚙️ Key Features & Data Quality Layer
1.Custom Audit Engine: Logs missing aircraft tail numbers, invalid timestamps, and referential integrity breaches into a dedicated logging table rather than failing silently.

2.Dimensional Modeling: Converts flat, raw flight records into a clean Star Schema with optimized Primary and Foreign keys for analytics.

3.Business Logic Handling: Standardizes military time integers (HHMM), parses negative departure delays to categorize early flights, and handles complex cancelled-flight logic.

🚀 How to Run the Pipeline
1.Clone the repository.

2.Download the raw dataset from the BTS On-Time Performance Database.

3.Ensure MySQL is running locally and update the database credentials in the Python configuration file.

4.Run etl_pipeline.py to execute the extraction, transformation, and loading phases.

5.Open the .pbix file in Power BI and refresh the data source to view the dashboard.

👤 Author
Khushi Goyal
