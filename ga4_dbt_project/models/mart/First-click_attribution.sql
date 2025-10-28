with base as (
  select
      s.user_pseudo_id as user_pseudo_id,
      s.channel,
      s.session_start,
      e.event_value
  from {{ ref('int_sessions') }} s
  join {{ ref('stg_events') }} e
    on s.user_pseudo_id = e.user_pseudo_id
  where e.event_name = 'purchase'
)
select distinct
    user_pseudo_id,
    first_value(channel) over (partition by user_pseudo_id order by session_start) as first_channel,
    min(session_start) over (partition by user_pseudo_id) as first_touch_time,
    sum(event_value) over (partition by user_pseudo_id) as revenue
from base
