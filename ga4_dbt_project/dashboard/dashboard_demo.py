import streamlit as st
from google.cloud import bigquery
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Attribution Dashboard", layout="wide")
st.title("Real-Time Attribution Dashboard")
st.caption("First vs Last Click Attribution | 14-Day Trends | Channel Breakdown | Live Stream")

client = bigquery.Client.from_service_account_json(
    r"D:\attribution_project\ga4_dbt_project\attribution-demo-1234-671daf5e5996.json"
)

# First Click Attribution
query_first = """
SELECT
  traffic_source.name AS first_channel,
  SUM(ecommerce.purchase_revenue_in_usd) AS total_revenue
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE event_name = 'purchase'
GROUP BY first_channel
ORDER BY total_revenue DESC
LIMIT 10
"""
df_first = client.query(query_first).to_dataframe(create_bqstorage_client=False)

# Last Click Attribution
query_last = """
SELECT
  traffic_source.name AS last_channel,
  SUM(ecommerce.purchase_revenue_in_usd) AS total_revenue
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE event_name = 'purchase'
GROUP BY last_channel
ORDER BY total_revenue DESC
LIMIT 10
"""
df_last = client.query(query_last).to_dataframe(create_bqstorage_client=False)

# 14-Day Revenue & Active Users
query_timeseries = """
SELECT
  DATE(TIMESTAMP_MICROS(event_timestamp)) AS day,
  COUNT(DISTINCT user_pseudo_id) AS active_users,
  SUM(ecommerce.purchase_revenue_in_usd) AS revenue
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE event_name = 'purchase'
GROUP BY day
ORDER BY day DESC
LIMIT 14
"""
df_timeseries = client.query(query_timeseries).to_dataframe(create_bqstorage_client=False)

# Live Events Stream (Recent 20)
query_live = """
SELECT
  TIMESTAMP_MICROS(event_timestamp) AS event_time,
  event_name,
  traffic_source.name AS channel,
  ecommerce.transaction_id,
  CONCAT(user_pseudo_id, "_", CAST(event_timestamp AS STRING)) AS event_id
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE event_name IN ('view_item', 'add_to_cart', 'purchase')
ORDER BY event_timestamp DESC
LIMIT 20
"""
df_live = client.query(query_live).to_dataframe(create_bqstorage_client=False)

# Track new events using session_state

if "seen_event_ids" not in st.session_state:
    st.session_state.seen_event_ids = set()

df_live["is_new"] = df_live["event_id"].apply(lambda x: x not in st.session_state.seen_event_ids)

st.session_state.seen_event_ids.update(df_live["event_id"].tolist())

df_live["dashboard_time"] = datetime.now()

# Streamlit Layout
col1, col2 = st.columns(2)
with col1:
    st.subheader("First-Click Attribution")
    st.bar_chart(df_first.set_index('first_channel')['total_revenue'])
with col2:
    st.subheader("Last-Click Attribution")
    st.bar_chart(df_last.set_index('last_channel')['total_revenue'])

# 14-Day Time Series
st.subheader("14-Day Revenue & Active Users")
st.line_chart(df_timeseries.set_index('day')[['revenue', 'active_users']])

# Channel Breakdown
st.subheader("Channel Breakdown (First vs Last Click)")
combined = pd.merge(df_first, df_last, left_on='first_channel', right_on='last_channel', how='outer')
combined = combined.fillna(0)
st.dataframe(combined)

# Live Stream Panel
st.subheader("Live Stream Events (Latest 20)")

st.dataframe(df_live[['event_time', 'event_name', 'channel', 'transaction_id', 'event_id', 'dashboard_time']])

st.success("Dashboard loaded successfully!")
