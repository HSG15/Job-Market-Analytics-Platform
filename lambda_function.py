import json
import os
import boto3
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

s3 = boto3.client("s3")

BUCKET_NAME = "job-market-tracker-hsg"
API_URL = "https://api.hirebase.org/v2/jobs/search"

def lambda_handler(event, context):
    try:
        now = datetime.now(ZoneInfo("Asia/Kolkata"))
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        current_time = now.strftime("%H-%M-%S")

        API_KEY = os.environ.get("HIREBASE_API_KEY")
        if not API_KEY:
            return {"statusCode": 500, "body": "API Key missing"}

        request_body = {
            "job_titles": ["Data Engineer", "Data Analyst", "Data Scientist"],
            "keywords": [
                "Python", "PySpark", "Apache Spark", "Java", "Scala", "SQL",
                "Databricks", "Kafka", "Airflow", "Azure", "AWS", "GCP",
                "ETL", "Hadoop", "Git", "GitHub", "Snowflake",
                "Docker", "Kubernetes", "Data Modeling", "Gen AI"
            ],
            "geo_locations": [{
                "city": "",
                "region": "",
                "country": "India"
            }],
            "date_posted_after": "today",
            "limit": 10
        }

        data = json.dumps(request_body).encode("utf-8")

        req = urllib.request.Request(API_URL, data=data, method="POST")

        # === HEADERS (Make it look like Postman) ===
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", "PostmanRuntime/7.36.0")
        req.add_header("x-api-key", API_KEY)
        req.add_header("Content-Length", str(len(data)))

        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                response_data = json.loads(response.read().decode())

        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            return {
                "statusCode": 500,
                "body": f"HTTP {e.code} - {error_body}"
            }

        s3_key = f"bronze/year={year}/month={month}/day={day}/jobs_{current_time}.json"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(response_data),
            ContentType="application/json"
        )

        return {
            "statusCode": 200,
            "body": f"Data saved to {s3_key}"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }