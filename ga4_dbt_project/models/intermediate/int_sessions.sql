with sessions as (
    select
        user_pseudo_id,
        min(event_timestamp) as session_start,
        max(event_timestamp) as session_end,
        channel
    from {{ ref('stg_events') }}
    group by user_pseudo_id, channel
)
select * from sessions
