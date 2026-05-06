
  
    

  create  table "pitt_ed"."analytics"."mart_wait_times__dbt_tmp"
  
  
    as
  
  (
    select
    v.esi_level,
    COUNT(*)                                                                AS patient_count,
    ROUND(AVG(EXTRACT(EPOCH FROM (e.event_time - v.arrival_time)) / 60)::NUMERIC, 1)
                                                                            AS avg_door_to_provider_mins,
    ROUND(MIN(EXTRACT(EPOCH FROM (e.event_time - v.arrival_time)) / 60)::NUMERIC, 1)
                                                                            AS min_mins,
    ROUND(MAX(EXTRACT(EPOCH FROM (e.event_time - v.arrival_time)) / 60)::NUMERIC, 1)
                                                                            AS max_mins
from "pitt_ed"."analytics"."stg_visits" v
join "pitt_ed"."public"."visit_events" e
    on v.visit_id = e.visit_id
    and e.event_type = 'provider_assigned'
group by v.esi_level
order by v.esi_level
  );
  