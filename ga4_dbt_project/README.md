# Project Title
GA4 Ecommerce Analytics with dbt and Realtime Dashboard

# Project Description

This project transforms GA4 ecommerce events from BigQuery using dbt.
It builds:
- Staging (stg_) models to clean raw GA4 events
- Intermediate (int_) models for sessions and user journeys
- Mart (mart_) models for revenue and first/last click attribution
It also includes:
- Streaming demo for live events
- Realtime dashboard prototype (Streamlit)

# Dataset

bigquery-public-data.ga4_obfuscated_sample_ecommerce
- Location: US
- Key Tables: events_*, items, customers

# dbt Models

- Layer	Tables	Description
- Staging	stg_events	Clean raw GA4 events & metadata
- Intermediate	int_sessions	Aggregate sessions, link users & events
- Mart	mart_first_click, mart_last_click	Analytics-ready tables, attribution models
- Tests	dbt tests on unique & not_null columns	Ensure data quality

# Streaming Demo

- Python script streams 5-20 sample events into BigQuery table `stream_events`
- Demonstrates incremental dbt updates and deduplication
- Deduplication handled via unique_key in incremental models
- Expected latency: ~1-2 seconds for streaming; 5-10 min for dbt incremental run

# Dashboard Prototype

- Streamlit app showing:
  - First vs Last Click totals
  - 14-day time series of revenue & active users
  - Channel breakdown
  - Live streamed events

# Run Instructions
venv\Scripts\activate
pip install -r requirements.txt


# Step 1: Configure BigQuery

Add your service account JSON and update profiles.yml with:
* project ID
* dataset name
* location (US)

# Set Google Credentials
Before running any dbt or dashboard command, set your service account JSON path:

- Windows: setx GOOGLE_APPLICATION_CREDENTIALS "C:\path\to\your_key.json"
- Mac/Linux: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your_key.json"

# Note: If you get an error like "Invalid JWT Signature" or "Unable to generate access token", 

- it means your service account key is expired or invalid.  
- Go to Google Cloud Console → IAM & Admin → Service Accounts → your existing account →    Create a new key,  
- download it, and update the path in your `profiles.yml` or environment variable.

# Step 2: Run dbt Models
dbt deps (Download dependencies)
dbt run  (Build staging → intermediate → mart)
dbt test (Run tests to ensure data quality)
dbt docs generate (Generate docs)
dbt docs serve   (Open in browser)

# Step 3: Run Streaming Demo
cd stream
python stream_events.py (Streams 5-20 sample events)

# Step 4: Launch Dashboard
cd dashboard
streamlit run dashboard_demo.py



