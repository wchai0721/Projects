
  create view "pitt_ed"."analytics"."stg_visits__dbt_tmp"
    
    
  as (
    select
    visit_id,
    patient_id,
    arrival_time,
    discharge_time,
    admission_type,
    esi_level,
    chief_complaint,
    department_id,
    EXTRACT(EPOCH FROM (discharge_time - arrival_time)) / 60 AS length_of_stay_mins
from "pitt_ed"."public"."visits"
  );