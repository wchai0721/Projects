-- Drop tables if rebuilding from scratch
DROP TABLE IF EXISTS interventions CASCADE;
DROP TABLE IF EXISTS diagnoses CASCADE;
DROP TABLE IF EXISTS dispositions CASCADE;
DROP TABLE IF EXISTS visit_events CASCADE;
DROP TABLE IF EXISTS visits CASCADE;
DROP TABLE IF EXISTS patients CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS staff CASCADE;

-- Departments
CREATE TABLE departments (
    department_id   INT PRIMARY KEY,
    name            VARCHAR(50) NOT NULL,
    floor           VARCHAR(5),
    bed_capacity    INT
);

-- Staff
CREATE TABLE staff (
    staff_id        INT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    role            VARCHAR(50),
    specialty       VARCHAR(50),
    shift_start     TIMESTAMP,
    shift_end       TIMESTAMP
);

-- Patients
CREATE TABLE patients (
    patient_id      INT PRIMARY KEY,
    first_name      VARCHAR(50),
    last_name       VARCHAR(50),
    age             INT,
    sex             CHAR(1),
    zip_code        VARCHAR(10),
    insurance_type  VARCHAR(20)
);

-- Visits
CREATE TABLE visits (
    visit_id        INT PRIMARY KEY,
    patient_id      INT REFERENCES patients(patient_id),
    arrival_time    TIMESTAMP,
    discharge_time  TIMESTAMP,
    admission_type  VARCHAR(20),
    esi_level       INT,
    chief_complaint VARCHAR(100),
    department_id   INT REFERENCES departments(department_id)
);

-- Visit events
CREATE TABLE visit_events (
    event_id        INT PRIMARY KEY,
    visit_id        INT REFERENCES visits(visit_id),
    event_type      VARCHAR(50),
    event_time      TIMESTAMP,
    department_id   INT REFERENCES departments(department_id),
    staff_id        INT REFERENCES staff(staff_id)
);

-- Interventions
CREATE TABLE interventions (
    intervention_id INT PRIMARY KEY,
    visit_id        INT REFERENCES visits(visit_id),
    intervention_type VARCHAR(50),
    intervention_time TIMESTAMP,
    staff_id        INT REFERENCES staff(staff_id)
);

-- Diagnoses
CREATE TABLE diagnoses (
    id              SERIAL PRIMARY KEY,
    visit_id        INT REFERENCES visits(visit_id),
    icd_code        VARCHAR(10),
    diagnosis_description VARCHAR(100),
    flag            VARCHAR(10)
);

-- Dispositions
CREATE TABLE dispositions (
    id              SERIAL PRIMARY KEY,
    visit_id        INT REFERENCES visits(visit_id),
    disposition     VARCHAR(50),
    disposition_time TIMESTAMP
);