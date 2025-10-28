from google.cloud import bigquery

client = bigquery.Client.from_service_account_json(
    r"D:\attribution_project\ga4_dbt_project\attribution-demo-1234-671daf5e5996.json"
)


for dataset in client.list_datasets():
    print(dataset.dataset_id)
