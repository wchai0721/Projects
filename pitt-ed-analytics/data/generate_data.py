import random
import csv
import os
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Config ---
SHIFT_START = datetime(2024, 3, 15, 7, 0)   # 7am - the Pitt starts here
NUM_PATIENTS = 180
NUM_STAFF = 24

# --- Reference data ---
DEPARTMENTS = [
    (1, "Trauma Bay",     "1",  4),
    (2, "Resus",          "1",  3),
    (3, "Fast Track",     "1", 12),
    (4, "Main ED",        "1", 20),
    (5, "Psych Hold",     "2",  6),
    (6, "Pediatric Bay",  "1",  6),
]

STAFF = [
    (1,  "Dr. Robby Robinavitch", "attending",  "trauma"),
    (2,  "Dr. Dana Evans",        "attending",  "general"),
    (3,  "Dr. Collins",           "attending",  "general"),
    (4,  "Dr. Langdon",           "resident",   "general"),
    (5,  "Dr. McKay",             "resident",   "trauma"),
    (6,  "Nurse Santos",          "nurse",      "trauma"),
    (7,  "Nurse Javadi",          "nurse",      "general"),
    (8,  "Nurse Collins",         "nurse",      "general"),
    (9,  "Nurse Park",            "nurse",      "pediatric"),
    (10, "Tech Barnes",           "tech",       "general"),
    (11, "Tech Cruz",             "tech",       "general"),
    (12, "Dr. Morin",             "attending",  "psych"),
    (13, "Dr. Patel",             "resident",   "general"),
    (14, "Dr. Whitfield",         "attending",  "general"),
    (15, "Nurse Okafor",          "nurse",      "general"),
    (16, "Nurse Chen",            "nurse",      "trauma"),
    (17, "Tech Morris",           "tech",       "trauma"),
    (18, "Dr. Singh",             "resident",   "general"),
    (19, "Nurse Reyes",           "nurse",      "general"),
    (20, "Dr. Abbott",            "attending",  "general"),
    (21, "Tech Flores",           "tech",       "general"),
    (22, "Nurse Kim",             "nurse",      "psych"),
    (23, "Dr. Tran",              "resident",   "general"),
    (24, "Nurse Wallace",         "nurse",      "general"),
]

CHIEF_COMPLAINTS = [
    ("chest pain",         1, "cardiac"),
    ("gunshot wound",      1, "trauma"),
    ("stab wound",         1, "trauma"),
    ("overdose",           2, "toxicology"),
    ("respiratory distress", 2, "pulmonary"),
    ("altered mental status", 2, "neuro"),
    ("stroke symptoms",    2, "neuro"),
    ("seizure",            2, "neuro"),
    ("abdominal pain",     3, "general"),
    ("fracture",           3, "orthopedic"),
    ("laceration",         4, "general"),
    ("fever",              4, "general"),
    ("back pain",          4, "general"),
    ("headache",           4, "general"),
    ("anxiety",            4, "psych"),
    ("urinary symptoms",   5, "general"),
    ("rash",               5, "general"),
    ("minor injury",       5, "general"),
]

INTERVENTIONS = {
    1: ["intubation", "blood transfusion", "chest tube", "central line", "FAST exam"],
    2: ["IV access", "cardiac monitor", "12-lead ECG", "blood transfusion", "defibrillation"],
    3: ["IV access", "oxygen therapy", "Narcan", "12-lead ECG", "labs ordered"],
    4: ["IV access", "labs ordered", "imaging ordered", "pain management", "IV fluids"],
    5: ["labs ordered", "oral medications", "wound care"],
}

DISPOSITIONS = {
    1: ["admitted_icu", "deceased"],
    2: ["admitted_icu", "admitted_floor", "deceased"],
    3: ["admitted_floor", "admitted_icu", "discharged"],
    4: ["discharged", "admitted_floor", "left_without_being_seen"],
    5: ["discharged", "left_without_being_seen"],
}

ICD_CODES = {
    "cardiac":      [("I21.9", "Acute MI"), ("I20.9", "Unstable angina"), ("I50.9", "Heart failure")],
    "trauma":       [("S21.9", "Open wound thorax"), ("S09.9", "Head injury"), ("T14.9", "Traumatic injury")],
    "toxicology":   [("T40.2", "Opioid overdose"), ("T51.0", "Alcohol toxicity"), ("T42.4", "Benzo overdose")],
    "pulmonary":    [("J18.9", "Pneumonia"), ("J44.1", "COPD exacerbation"), ("J96.0", "Acute resp failure")],
    "neuro":        [("G40.9", "Epilepsy/seizure"), ("I63.9", "Cerebral infarction"), ("R41.3", "AMS")],
    "general":      [("R10.9", "Abdominal pain"), ("M54.5", "Low back pain"), ("R51", "Headache")],
    "orthopedic":   [("S52.5", "Radius fracture"), ("S82.2", "Tibia fracture"), ("M79.3", "Soft tissue disorder")],
    "psych":        [("F41.1", "Generalized anxiety"), ("F32.9", "Major depression"), ("F20.9", "Schizophrenia")],
}

def rand_minutes(lo, hi):
    return timedelta(minutes=random.randint(lo, hi))

def write_csv(filename, rows, headers):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)
    print(f"  wrote {len(rows)} rows -> {filename}")

def main():
    print("Generating Pitt ED shift data...")

    # departments
    write_csv("departments.csv", DEPARTMENTS,
              ["department_id","name","floor","bed_capacity"])

    # staff
    write_csv("staff.csv",
              [(s[0], s[1], s[2], s[3], SHIFT_START, SHIFT_START + timedelta(hours=15))
               for s in STAFF],
              ["staff_id","name","role","specialty","shift_start","shift_end"])

    # patients + visits + events + interventions + diagnoses + dispositions
    patients, visits, events, interventions_rows, diagnoses, dispositions = [], [], [], [], [], []

    arrival_time = SHIFT_START
    event_id = 1
    intervention_id = 1

    for pid in range(1, NUM_PATIENTS + 1):
        # space arrivals across 15 hours, busier mid-shift
        hour_weight = [1,1,2,2,3,3,3,2,2,2,1,1,1,1,1]
        hour_offset = random.choices(range(15), weights=hour_weight)[0]
        arrival_time = SHIFT_START + timedelta(hours=hour_offset,
                                               minutes=random.randint(0, 59))

        complaint, esi, specialty = random.choice(CHIEF_COMPLAINTS)

        # assign department based on ESI
        dept_map = {1: 2, 2: 1, 3: 4, 4: 3, 5: 3}
        if complaint in ("gunshot wound", "stab wound"):
            dept_id = 1
        elif specialty == "psych":
            dept_id = 5
        elif esi <= 2 and random.random() < 0.4:
            dept_id = 2
        else:
            dept_id = dept_map.get(esi, 4)

        age = random.randint(1, 89)
        if age < 18:
            dept_id = 6

        ins = random.choice(["Medicare", "Medicaid", "Private", "Uninsured", "VA"])

        patients.append((pid, fake.first_name(), fake.last_name(), age,
                         random.choice(["M", "F"]), fake.zipcode(), ins))

        visit_id = pid
        admit_type = random.choices(
            ["emergency", "walk-in", "transfer"],
            weights=[60, 35, 5])[0]

        # triage
        t_triage = arrival_time + rand_minutes(2, 18)
        # provider
        t_provider = t_triage + rand_minutes(8 if esi <= 2 else 20, 45 if esi >= 4 else 25)
        # labs/imaging (not always)
        t_labs = t_provider + rand_minutes(5, 20)
        t_imaging = t_labs + rand_minutes(15, 60) if esi <= 3 else None
        # consult (ESI 1-2 only)
        t_consult = (t_imaging or t_labs) + rand_minutes(20, 90) if esi <= 2 else None
        # disposition decision
        t_dispo_decision = (t_consult or t_imaging or t_labs) + rand_minutes(10, 60)
        # discharge/admit
        t_discharge = t_dispo_decision + rand_minutes(15, 120)

        visits.append((visit_id, pid, arrival_time, t_discharge,
                       admit_type, esi, complaint, dept_id))

        for etype, etime in [
            ("arrival",            arrival_time),
            ("triage",             t_triage),
            ("provider_assigned",  t_provider),
            ("labs_ordered",       t_labs),
            ("imaging_ordered",    t_imaging),
            ("consult_called",     t_consult),
            ("disposition_decision", t_dispo_decision),
            ("discharge",          t_discharge),
        ]:
            if etime is None:
                continue
            staff_id = random.choice([s[0] for s in STAFF])
            events.append((event_id, visit_id, etype, etime, dept_id, staff_id))
            event_id += 1

        # interventions
        for intv in random.sample(INTERVENTIONS[esi], k=min(len(INTERVENTIONS[esi]),
                                                             random.randint(1, 3))):
            intv_time = t_provider + rand_minutes(5, 30)
            staff_id = random.choice([s[0] for s in STAFF])
            interventions_rows.append((intervention_id, visit_id, intv,
                                       intv_time, staff_id))
            intervention_id += 1

        # diagnosis
        icd_options = ICD_CODES.get(specialty, ICD_CODES["general"])
        code, desc = random.choice(icd_options)
        diagnoses.append((visit_id, code, desc, "primary"))
        if random.random() < 0.4:
            sec_code, sec_desc = random.choice(ICD_CODES["general"])
            diagnoses.append((visit_id, sec_code, sec_desc, "secondary"))

        # disposition
        dispo = random.choices(
            DISPOSITIONS[esi],
            weights=[1] * len(DISPOSITIONS[esi]))[0]
        dispositions.append((visit_id, dispo, t_discharge))

    write_csv("patients.csv",    patients,
              ["patient_id","first_name","last_name","age","sex","zip_code","insurance_type"])
    write_csv("visits.csv",      visits,
              ["visit_id","patient_id","arrival_time","discharge_time",
               "admission_type","esi_level","chief_complaint","department_id"])
    write_csv("visit_events.csv", events,
              ["event_id","visit_id","event_type","event_time","department_id","staff_id"])
    write_csv("interventions.csv", interventions_rows,
              ["intervention_id","visit_id","intervention_type","intervention_time","staff_id"])
    write_csv("diagnoses.csv",   diagnoses,
              ["visit_id","icd_code","diagnosis_description","flag"])
    write_csv("dispositions.csv", dispositions,
              ["visit_id","disposition","disposition_time"])

    print("Done.")

if __name__ == "__main__":
    main()