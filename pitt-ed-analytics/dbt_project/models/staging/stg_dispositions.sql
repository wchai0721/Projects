select
    visit_id,
    disposition,
    disposition_time
from {{ source('public', 'dispositions') }}