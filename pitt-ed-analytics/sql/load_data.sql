\COPY departments   FROM '/Users/wenchai/projects/pitt-ed-analytics/data/departments.csv'   CSV HEADER;
\COPY staff         FROM '/Users/wenchai/projects/pitt-ed-analytics/data/staff.csv'         CSV HEADER;
\COPY patients      FROM '/Users/wenchai/projects/pitt-ed-analytics/data/patients.csv'      CSV HEADER;
\COPY visits        FROM '/Users/wenchai/projects/pitt-ed-analytics/data/visits.csv'        CSV HEADER;
\COPY visit_events  FROM '/Users/wenchai/projects/pitt-ed-analytics/data/visit_events.csv'  CSV HEADER;
\COPY interventions FROM '/Users/wenchai/projects/pitt-ed-analytics/data/interventions.csv' CSV HEADER;
\COPY diagnoses     FROM '/Users/wenchai/projects/pitt-ed-analytics/data/diagnoses.csv'     CSV HEADER;
\COPY dispositions  FROM '/Users/wenchai/projects/pitt-ed-analytics/data/dispositions.csv'  CSV HEADER;