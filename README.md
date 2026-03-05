# 🚀 AWS Data Engineering Project – Job Market Data Pipeline

This project demonstrates a real-world **end-to-end data engineering pipeline on AWS** using the **Medallion Architecture (Bronze → Silver → Gold)**.

The pipeline collects job market data from an external API, processes it using AWS services, and makes it available for analytics and dashboarding.

---

# 📌 Project Architecture

<img width="1061" height="516" alt="image" src="https://github.com/user-attachments/assets/2f9c93b5-163a-4d4f-b4a3-9b67da3fc879" />

**Flow:**

API (Hirebase / Adzuna)  
→ AWS Lambda  
→ S3 (Bronze Layer)  
→ AWS Glue (ETL)  
→ S3 (Silver Layer)  
→ AWS Glue (Aggregation)  
→ S3 (Gold Layer)  
→ Glue Crawler  
→ Athena  
→ Power BI / QuickSight  

---

# 🧰 Tools & Services Used

- **AWS Lambda** – API ingestion (serverless compute)
- **Amazon S3** – Data lake storage (Bronze, Silver, Gold layers)
- **AWS Glue (PySpark)** – Data transformation and aggregation
- **AWS Glue Crawler** – Schema detection
- **AWS Glue Data Catalog** – Metadata management
- **Amazon Athena** – SQL query engine on S3
- **Power BI / Amazon QuickSight** – Data visualization

---

# 🏗️ Medallion Architecture

## 🥉 Bronze Layer (Raw Data)
- Stores raw JSON response from job API
- Partitioned by: bronze/year=YYYY/month=MM/day=DD/
- No transformations applied

---

## 🥈 Silver Layer (Cleaned Data)
- Reads raw JSON from Bronze
- Cleans and standardizes:
- job_title
- company
- location
- salary
- skills
- Removes duplicates
- Converts to **Parquet format**
- Partitioned by date

---

## 🥇 Gold Layer (Analytics-Ready Data)
- Aggregated datasets for reporting:
- Role-wise job demand
- Location-wise job postings
- Top skills demand
- Role vs Skills mapping
- Stored in optimized Parquet format
- Ready for SQL queries and dashboards

---

# 🔄 Project Flow (Step-by-Step)

## 1️⃣ S3 Data Lake Setup

Created S3 bucket: job-market-tracker-hsg

Folder structure: bronze/ silver/ gold/


---

## 2️⃣ API Ingestion using AWS Lambda

- Created Lambda function
- Connected to Job API (Hirebase / Adzuna)
- Stored API response in Bronze layer as JSON
- Used CloudWatch for monitoring logs
- (Optional) Scheduled using EventBridge for daily execution

---

## 3️⃣ Data Transformation using AWS Glue (Bronze → Silver)

- Created Glue ETL job using PySpark
- Read JSON files from Bronze
- Cleaned and structured data
- Standardized job roles
- Removed duplicates
- Wrote output to Silver layer in Parquet format

---

## 4️⃣ Data Aggregation using AWS Glue (Silver → Gold)

- Created second Glue job
- Built aggregated datasets:
  - Total jobs per role
  - Jobs per location
  - Top skills demand
- Saved analytics-ready data in Gold layer

---

## 5️⃣ Glue Crawler & Data Catalog

- Created Glue Database: `job_market_db`
- Configured Glue Crawler to scan Gold layer
- Automatically created tables in Data Catalog

---

## 6️⃣ Querying using Amazon Athena

Example query:

```sql
SELECT role_category, SUM(total_postings)
FROM role_demand
GROUP BY role_category
ORDER BY 2 DESC;
```
Athena reads data directly from S3 without loading into a database.

## 7️⃣ Dashboard Layer (Optional)

Gold layer can be connected to:

- Power BI (via Athena ODBC)
- Amazon QuickSight

Dashboard examples:

- 📈 Role demand trends
- 📍 Location-wise job postings
- 🔥 Top in-demand skills
