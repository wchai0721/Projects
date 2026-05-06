with readmissions as (
    select
        v1.patient_id,
        v1.visit_id                     as first_visit,
        v2.visit_id                     as readmit_visit,
        v1.discharge_time               as first_discharge,
        v2.arrival_time                 as readmit_arrival,
        EXTRACT(EPOCH FROM (
            v2.arrival_time - v1.discharge_time
        )) / 86400                      as days_between
    from "pitt_ed"."analytics"."stg_visits" v1
    join "pitt_ed"."analytics"."stg_visits" v2
        on v1.patient_id = v2.patient_id
        and v2.arrival_time > v1.discharge_time
        and EXTRACT(EPOCH FROM (
            v2.arrival_time - v1.discharge_time
        )) / 86400 <= 30
        and v1.visit_id <> v2.visit_id
)
select
    p.insurance_type,
    d.diagnosis_description,
    COUNT(*)                            as readmissions,
    ROUND(AVG(r.days_between)::NUMERIC, 1)
                                        as avg_days_to_readmit
from readmissions r
join "pitt_ed"."analytics"."stg_patients" p on r.patient_id = p.patient_id
join "pitt_ed"."public"."diagnoses" d
    on r.first_visit = d.visit_id
    and d.flag = 'primary'
group by p.insurance_type, d.diagnosis_description
order by readmissions desc