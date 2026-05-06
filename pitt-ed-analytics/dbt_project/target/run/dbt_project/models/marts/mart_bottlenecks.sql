
  
    

  create  table "pitt_ed"."analytics"."mart_bottlenecks__dbt_tmp"
  
  
    as
  
  (
    with event_durations as (
    select
        visit_id,
        event_type,
        event_time,
        LEAD(event_time) OVER (
            PARTITION BY visit_id
            ORDER BY event_time
        )                               as next_event_time,
        LEAD(event_type) OVER (
            PARTITION BY visit_id
            ORDER BY event_time
        )                               as next_event_type
    from "pitt_ed"."analytics"."stg_visit_events"
)
select
    event_type                          as stage,
    next_event_type                     as next_stage,
    COUNT(*)                            as transitions,
    ROUND(AVG(EXTRACT(EPOCH FROM (next_event_time - event_time)) / 60)::NUMERIC, 1)
                                        as avg_mins,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (
        ORDER BY EXTRACT(EPOCH FROM (next_event_time - event_time)) / 60
    )::NUMERIC, 1)                      as median_mins,
    ROUND(MAX(EXTRACT(EPOCH FROM (next_event_time - event_time)) / 60)::NUMERIC, 1)
                                        as max_mins
from event_durations
where next_event_time is not null
group by event_type, next_event_type
order by avg_mins desc
  );
  