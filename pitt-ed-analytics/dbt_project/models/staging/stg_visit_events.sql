select
    event_id,
    visit_id,
    event_type,
    event_time,
    department_id,
    staff_id
from {{ source('public', 'visit_events') }}