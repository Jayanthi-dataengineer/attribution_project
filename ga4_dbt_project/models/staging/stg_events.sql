with raw as (
    select
        event_name,
        event_timestamp,
        user_pseudo_id,
        SAFE_CAST(json_extract_scalar(ep.value.string_value, '$') AS FLOAT64) as event_value,
        platform,
        traffic_source.source as channel
    from `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`,
         unnest(event_params) as ep
    where event_name in ('purchase', 'add_to_cart', 'page_view')
)
select * from raw
