select
    patient_id,
    first_name || ' ' || last_name  as patient_name,
    age,
    sex,
    zip_code,
    insurance_type
from "pitt_ed"."public"."patients"