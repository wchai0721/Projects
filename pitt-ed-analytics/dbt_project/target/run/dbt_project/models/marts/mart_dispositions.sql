
  
    

  create  table "pitt_ed"."analytics"."mart_dispositions__dbt_tmp"
  
  
    as
  
  (
    select
    v.esi_level,
    d.disposition,
    COUNT(*)                            as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (
        PARTITION BY v.esi_level
    )::NUMERIC, 1)                      as pct_of_esi_level
from "pitt_ed"."analytics"."stg_visits" v
join "pitt_ed"."analytics"."stg_dispositions" d on v.visit_id = d.visit_id
group by v.esi_level, d.disposition
order by v.esi_level, count desc
  );
  