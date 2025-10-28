from google.cloud import bigquery
from datetime import datetime
import uuid, random, json
import time

client = bigquery.Client.from_service_account_json(
    r"D:\attribution_project\ga4_dbt_project\attribution-demo-1234-671daf5e5996.json")

table_id = "attribution-demo-1234.ga4_dbt_demo.events_stream_demo"

sample_events = [
    {"event_name": "purchase", "item_id": "A1", "price": 199},
    {"event_name": "add_to_cart", "item_id": "B2", "price": 49},
    {"event_name": "page_view", "item_id": None, "price": 0}
]

rows_to_insert = []

for i in range(20):
    event_choice = random.choice(sample_events)

    event_timestamp = datetime.now().isoformat()

    row = {
        "event_name": event_choice["event_name"],
        "event_timestamp": event_timestamp,
        "user_pseudo_id": str(uuid.uuid4()),
        "event_params": json.dumps(event_choice),
        "platform": random.choice(["web", "ios", "android"]),
        "traffic_source": random.choice(["google", "email", "organic"])
    }

    rows_to_insert.append(row)

    time.sleep(0.05)

job = client.load_table_from_json(rows_to_insert, table_id)
job.result() 

print(f"Inserted {len(rows_to_insert)} rows successfully!")
