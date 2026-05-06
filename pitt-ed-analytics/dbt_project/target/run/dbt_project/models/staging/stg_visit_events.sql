
  create view "pitt_ed"."analytics"."stg_visit_events__dbt_tmp"
    
    
  as (
    select
    event_id,
    visit_id,
    event_type,
    event_time,
    department_id,
    staff_id
from "pitt_ed"."public"."visit_events"
  );