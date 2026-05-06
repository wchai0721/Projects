
  create view "pitt_ed"."analytics"."stg_dispositions__dbt_tmp"
    
    
  as (
    select
    visit_id,
    disposition,
    disposition_time
from "pitt_ed"."public"."dispositions"
  );