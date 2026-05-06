select
    s.name                                          as staff_name,
    s.role,
    DATE_TRUNC('hour', ve.event_time)               as shift_hour,
    EXTRACT(HOUR FROM ve.event_time)                as hour_of_shift,
    COUNT(DISTINCT ve.visit_id)                     as active_patients
from "pitt_ed"."public"."visit_events" ve
join "pitt_ed"."public"."staff" s on ve.staff_id = s.staff_id
where s.role in ('attending', 'resident')
group by s.name, s.role, shift_hour, hour_of_shift
order by shift_hour, active_patients desc