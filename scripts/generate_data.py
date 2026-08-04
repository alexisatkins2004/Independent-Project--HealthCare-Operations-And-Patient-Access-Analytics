"""
Generate synthetic source data for the Seattle Grace Health Network 
Power BI project.

The data intentionally includes a small number of quality issues so 
they can be identified and corrected in Power Query.
"""

pip install pandas numpy openpyxl

# ========================================================================
# PART 1: IMPORT PYTHON TOOLS 
# ========================================================================

from pathlib import Path # Helps with folders and file locations.

import random # Allows fake value generation. 

import json # For Clinic data.

from datetime import date, timedelta # Helps create dates.

import pandas as pd # Helps create tables. 

import numpy as np # Allows random number generation.

# ========================================================================
# PART 2: BASIC SETTINGS
# ========================================================================

# Ensures fake data stays the same every time script runs.
random.seed(42)
np.random.seed(42)

# Tells where to save finished data files (data/raw/).
OUTPUT_FOLDER = Path(__file__).resolve().parent.parent / "data" / "raw"

# ========================================================================
# PART 3: CHOOSE HOW MUCH DATA TO CREATE
# ========================================================================

NUMBER_OF_PATIENTS = 500
NUMBER_OF_PROVIDERS = 48
NUMBER_OF_APPOINTMENTS_PER_MONTH = 800

# ========================================================================
# PART 4: CREATE LISTS OF POSSIBLE VALUES
# ========================================================================

# Establishes department IDs.
departments = [
    ("D01", "Primary Care"),
    ("D02", "Cardiology"),
    ("D03", "Dermatology"),
    ("D04", "Orthopedics"),
    ("D05", "Behavioral Health"),
    ("D06", "Pediatrics"),
]

# Fake clinic information.
clinic_data = [
    {
        "ClinicID": "C01",
        "ClinicName": "Boston Central Clinic",
        "City": "Boston",
        "State": "MA",
        "Region": "Northeast",
        "TreatmentRooms": 18,
        "DailyAppointmentCapacity": 180,
    },
    {
        "ClinicID": "C02",
        "ClinicName": "Cambridge Health Center",
        "City": "Cambridge",
        "State": "MA",
        "Region": "Northeast",
        "TreatmentRooms": 14,
        "DailyAppointmentCapacity": 140,
    },
    {
        "ClinicID": "C03",
        "ClinicName": "Providence Outpatient Center",
        "City": "Providence",
        "State": "RI",
        "Region": "Northeast",
        "TreatmentRooms": 12,
        "DailyAppointmentCapacity": 120,
    },
    {
        "ClinicID": "C04",
        "ClinicName": "Hartford Medical Plaza",
        "City": "Hartford",
        "State": "CT",
        "Region": "Northeast",
        "TreatmentRooms": 15,
        "DailyAppointmentCapacity": 150,
    },
    {
        "ClinicID": "C05",
        "ClinicName": "Philadelphia Center City",
        "City": "Philadelphia",
        "State": "PA",
        "Region": "Mid-Atlantic",
        "TreatmentRooms": 20,
        "DailyAppointmentCapacity": 210,
    },
    {
        "ClinicID": "C06",
        "ClinicName": "Baltimore Harbor Clinic",
        "City": "Baltimore",
        "State": "MD",
        "Region": "Mid-Atlantic",
        "TreatmentRooms": 13,
        "DailyAppointmentCapacity": 130,
    },
    {
        "ClinicID": "C07",
        "ClinicName": "Charlotte Health Center",
        "City": "Charlotte",
        "State": "NC",
        "Region": "Southeast",
        "TreatmentRooms": 16,
        "DailyAppointmentCapacity": 165,
    },
    {
        "ClinicID": "C08",
        "ClinicName": "Atlanta Midtown Clinic",
        "City": "Atlanta",
        "State": "GA",
        "Region": "Southeast",
        "TreatmentRooms": 17,
        "DailyAppointmentCapacity": 175,
    },
    {
        "ClinicID": "C09",
        "ClinicName": "Chicago Lakeside Clinic",
        "City": "Chicago",
        "State": "IL",
        "Region": "Midwest",
        "TreatmentRooms": 19,
        "DailyAppointmentCapacity": 195,
    },
    {
        "ClinicID": "C10",
        "ClinicName": "Denver Regional Clinic",
        "City": "Denver",
        "State": "CO",
        "Region": "Mountain",
        "TreatmentRooms": 14,
        "DailyAppointmentCapacity": 145,
    },
]

# Fake demographic information.
patient_locations = [
    ("Boston", "MA", "02108"),
    ("Cambridge", "MA", "02139"),
    ("Providence", "RI", "02903"),
    ("Hartford", "CT", "06103"),
    ("Philadelphia", "PA", "19103"),
    ("Baltimore", "MD", "21201"),
    ("Charlotte", "NC", "28202"),
    ("Atlanta", "GA", "30303"),
    ("Chicago", "IL", "60601"),
    ("Denver", "CO", "80202"),
]

genders = [
    "Female",
    "Male",
    "Nonbinary",
    "Prefer Not to Say",
]

first_names = [
    "Avery", "Jordan", "Taylor", "Morgan", "Riley", "Cameron",
    "Alex", "Casey", "Jamie", "Quinn", "Parker", "Reese",
    "Maya", "Sofia", "Elena", "Nora", "Liam", "Noah",
    "Ethan", "Lucas",
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
    "Miller", "Davis", "Wilson", "Anderson", "Thomas", "Moore",
    "Martin", "Jackson", "Thompson", "White", "Harris", "Clark",
]

insurance_types = [
    "Commercial",
    "Medicare",
    "Medicaid",
    "Self-Pay",
]

# Establishes department provider specialties.
specialties_by_department = {
    "D01": ["Family Medicine", "Internal Medicine"],
    "D02": ["General Cardiology", "Preventive Cardiology"],
    "D03": ["General Dermatology", "Medical Dermatology"],
    "D04": ["Sports Medicine", "Joint Care"],
    "D05": ["Psychology", "Psychiatry", "Counseling"],
    "D06": ["General Pediatrics", "Adolescent Medicine"],
}

# Establishes service categories.
service_rows = [
    ("S001", "Annual Physical", "Primary Care", 225.00, 105.00, 45),
    ("S002", "Primary Care Follow-Up", "Primary Care", 145.00, 68.00, 30),
    ("S003", "Urgent Office Visit", "Primary Care", 185.00, 88.00, 30),
    ("S004", "Preventive Screening", "Primary Care", 275.00, 130.00, 45),

    ("S005", "Cardiology Consultation", "Cardiology", 425.00, 210.00, 60),
    ("S006", "ECG Review", "Cardiology", 180.00, 80.00, 30),
    ("S007", "Hypertension Follow-Up", "Cardiology", 210.00, 95.00, 30),
    ("S008", "Cardiac Risk Assessment", "Cardiology", 350.00, 170.00, 45),

    ("S009", "Skin Examination", "Dermatology", 245.00, 110.00, 30),
    ("S010", "Acne Consultation", "Dermatology", 195.00, 82.00, 30),
    ("S011", "Rash Evaluation", "Dermatology", 210.00, 90.00, 30),
    ("S012", "Lesion Follow-Up", "Dermatology", 175.00, 74.00, 20),

    ("S013", "Orthopedic Consultation", "Orthopedics", 330.00, 155.00, 45),
    ("S014", "Sports Injury Visit", "Orthopedics", 285.00, 130.00, 45),
    ("S015", "Joint Pain Follow-Up", "Orthopedics", 215.00, 98.00, 30),
    ("S016", "Mobility Assessment", "Orthopedics", 250.00, 118.00, 40),

    ("S017", "Therapy Session", "Behavioral Health", 190.00, 92.00, 50),
    ("S018", "Psychiatric Consultation", "Behavioral Health", 375.00, 185.00, 60),
    ("S019", "Medication Follow-Up", "Behavioral Health", 165.00, 75.00, 30),
    ("S020", "Behavioral Health Assessment", "Behavioral Health", 310.00, 150.00, 60),

    ("S021", "Well-Child Visit", "Pediatrics", 205.00, 95.00, 40),
    ("S022", "Pediatric Sick Visit", "Pediatrics", 175.00, 80.00, 30),
    ("S023", "Vaccination Visit", "Pediatrics", 130.00, 55.00, 20),
    ("S024", "Developmental Follow-Up", "Pediatrics", 220.00, 102.00, 40),
]

# Connects each service category to a department ID.
department_id_by_category = {
    "Primary Care": "D01",
    "Cardiology": "D02",
    "Dermatology": "D03",
    "Orthopedics": "D04",
    "Behavioral Health": "D05",
    "Pediatrics": "D06",
}

# ========================================================================
# PART 5: SMALL HELPER FUNCTIONS
# ========================================================================

# Creates random dates between a starting date and an ending date.
def create_random_date(start_date, end_date):
    number_of_days = (end_date - start_date).days
    random_number = random.randint(0, number_of_days)
    return start_date + timedelta(days=random_number)

# Creates one fake provider name.
def create_random_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Finds the final day of the month. 
def get_last_day_of_month(year, month):
    if month == 12:
        return date(year + 1, 1, 1) - timedelta(days=1)
    return date(year, month + 1, 1) - timedelta(days=1)

# Turns a number of minutes into a time. 
def minutes_to_time_text(total_minutes):
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours:02d}:{minutes:02d}"

# ========================================================================
# PART 6: CREATE PATIENT TABLE
# ========================================================================

# Creates patient demographics.
def create_patients():
    
    # Creates empty patient list.
    patient_list = []

    # Creates one patient at a time until goal is reached.
    for patient_number in range(1, NUMBER_OF_PATIENTS + 1): 

        # Picks one fake city, state, and postal code.
        city, state, postal_code = random.choice(patient_locations)

        # Creates column names and random column data.
        patient = {
            "PatientID": f"PT{patient_number:04d}",
            "BirthYear": random.randint(1940, 2020),
            "Gender": random.choices(
                genders,
                weights=[47, 47, 3, 3],
                k=1,
            )[0],
            "City": city,
            "State": state,
            "PostalCode": postal_code,
            "InsuranceType": random.choices(
                insurance_types,
                weights=[52, 20, 20, 8],
                k=1,
            )[0],
            "RegistrationDate": create_random_date(
                date(2018, 1, 1),
                date(2025, 12, 31),
            ).isoformat(),
        }

        patient_list.append(patient)

    # Turn list into a table.
    patients = pd.DataFrame(patient_list)

    # ========================================================================
    # INTENTIONAL DATA QUALITY PROBLEMS
    # ========================================================================

    # Adds one duplicate PatientID.
    duplicate_patient = patients.iloc[[24]].copy()
    patients = pd.concat(
        [patients, duplicate_patient],
        ignore_index=True,
    )

    # Makes a few insurance values blank.
    blank_rows = random.sample(
        list(patients.index),
        5,
    )
    patients.loc[blank_rows, "InsuranceType"] = None

    # Writes one state in full instead of using the abbreviation.
    patients.loc[10, "State"] = "Massachusetts"

    return patients

# ========================================================================
# PART 7: CREATE PROVIDER TABLE
# ========================================================================

# Creates provider information. 
def create_providers():
    
    # Creates empty provider list.
    provider_list = []

    # Creates list with only Departnment IDs.
    department_ids = [
        department_id
    
        # Items in "departments" have two values. Only want Department ID.
        for department_id, department_name in departments
    ]

    # Creates one provider at a time until goal is reached.
    for provider_number in range(1, NUMBER_OF_PROVIDERS + 1):

        # Spreads providers across the six departments.
        department_id = department_ids[
            (provider_number - 1) % len(department_ids)
        ]

        # Creates column names and random column data.
        provider = {
            "ProviderID": f"PR{provider_number:03d}",
            "ProviderName": create_random_name(),
            "Specialty": random.choice(
                specialties_by_department[department_id]
            ),
            "DepartmentID": department_id,
            "HireDate": create_random_date(
                date(2012, 1, 1),
                date(2025, 6, 30),
            ).isoformat(),
            "EmploymentType": random.choices(
                ["Full-Time", "Part-Time", "Contract"],
                weights=[70, 24, 6],
                k=1,
            )[0],
            "WeeklyCapacityHours": random.choice(
                [20, 24, 30, 32, 36, 40]
            ),
        }

        provider_list.append(provider)

    providers = pd.DataFrame(provider_list)

    # ========================================================================
    # INTENTIONAL DATA QUALITY PROBLEMS
    # ========================================================================

    # Adds an extra space to a few ProviderID values.
    providers.loc[3, "ProviderID"] = "PR004 "
    providers.loc[17, "ProviderID"] = " PR018"

    return providers

# ========================================================================
# PART 8: CREATE THE CLINIC TABLE
# ========================================================================

# Creates clinic information.
def create_clinics():
    
    # Uses exact columns from the clinic data dictionary to create table.
    
    return pd.DataFrame(clinic_data)

# ========================================================================
# PART 9: CREATE THE SERVICE TABLE
# ========================================================================

# Creates service information.
def create_services():
   
    # Uses exact columns from the service data dictionary to create table.

    # Creates column names.
    services = pd.DataFrame(
        service_rows,
        columns=[
            "ServiceID",
            "ServiceName",
            "ServiceCategory",
            "StandardPrice",
            "EstimatedCost",
            "StandardDurationMinutes",
        ],
    )

    # ========================================================================
    # INTENTIONAL DATA QUALITY PROBLEMS
    # ========================================================================

    # Adds a dollar sign to one price.
    services["StandardPrice"] = services["StandardPrice"].astype(object)
    services.loc[4, "StandardPrice"] = "$425.00"

    return services

# ========================================================================
# PART 10: CREATE THE DEPARTMENT BUDGET TABLE
# ========================================================================

# Creates department budget information.
def create_department_budget():
   
    # Uses exact columns from the department budget dictionary.

    # Creates an empty budget list.
    budget_list = []

    # Creates months list.
    months = ["January", "February", "March"]

    # Loops through each department in the departments list.
    # Each item in the list contains two items. Only want department ID.
    for department_id, department_name in departments:
        
        # Loops through every month in the months list for each department.
        # Creates one budget entry for every department for each month.
        for month in months:
            
            # Adds new dictionary (row of data) to the budget list.
            # Each dictionary is the monthly budget for each department.
            budget_list.append(
                {
                    "DepartmentID": department_id,
                    "Month": month,
                    "Budget": round(
                        random.uniform(85000, 170000),
                        2,
                    ),
                }
            )

    budgets = pd.DataFrame(budget_list)

    # ========================================================================
    # INTENTIONAL DATA QUALITY PROBLEMS
    # ========================================================================

    # Adds a dollar sign to one budget value.
    budgets["Budget"] = budgets["Budget"].astype(object)
    budgets.loc[5, "Budget"] = "$125,000.00"

    return budgets

# ========================================================================
# PART 11: CREATE ONE MONTH OF APPOINTMENTS
# ========================================================================

# Creates appointments for the month.
def create_appointments_for_month(
    year,
    month,
    patients,
    providers,
    services,
    first_appointment_number,
):

    # Creates one monthly appointment file to be used three times.

    # Creates empty appointment list.
    appointment_list = []

    # Uses clean ID lists internally so the relationships mostly work.
    
    # Gets PatientID from patient DataFrame and converts to string.
    patient_ids = (
        patients["PatientID"]
        .astype(str)
        .str.strip()
        .drop_duplicates()
        .tolist()
    )

    # Creates copy of provider DataFrame and converts to string.
    clean_providers = providers.copy()
    clean_providers["ProviderID"] = (
        clean_providers["ProviderID"]
        .astype(str)
        .str.strip()
    )

    # Creates list containing all ClinicIDs from the clinic_data list.
    clinic_ids = [
    clinic_ids = [
        clinic["ClinicID"]

        # Loops through every clinic in the clinic_data list. 
        for clinic in clinic_data
    ]

    # Determines the first and last day of a specified month.
    first_day = date(year, month, 1)
    last_day = get_last_day_of_month(year, month)

    # Loops through the specified number of appointments to generate appointment records for the month.
    for row_number in range(NUMBER_OF_APPOINTMENTS_PER_MONTH):

        # Picks one provider.
        provider = clean_providers.sample(n=1).iloc[0]
        provider_id = provider["ProviderID"]
        department_id = provider["DepartmentID"]

        # Finds the department name connected to the department ID.
        department_name = next(
            name
            for dept_id, name in departments
            if dept_id == department_id
        )

        # Finds services that belong to the provider department.
        possible_services = services[
            services["ServiceCategory"] == department_name
        ]

        # Picks one service.
        service = possible_services.sample(n=1).iloc[0]

        # Chooses a random appointment date.
        appointment_date = create_random_date(
            first_day,
            last_day,
        )

        # Ensures booking date happens before the appointment date.
        booking_date = appointment_date - timedelta(
            days=random.randint(0, 60)
        )

        # Chooses appointment status.
        appointment_status = random.choices(
            ["Completed", "Canceled", "No-Show", "Scheduled"],
            weights=[72, 10, 8, 10],
            k=1,
        )[0]

        # Chooses scheduled time between 8:00 AM and 5:00 PM.
        scheduled_minutes = random.choice(
            list(range(8 * 60, 17 * 60 + 1, 15))
        )

        # Shows completed visits actual times, durations, and satisfaction scores.
        
        # If appointment status is Complete.
        if appointment_status == "Completed":

            # Generates random wait time as an integer.
            wait_time = int(
            wait_time = int(
                np.clip(
                    np.random.normal(14, 11),
                    -5,
                    75,
                )
            )

            # Generates actual time.
            actual_minutes = scheduled_minutes + wait_time

            # Generates total visit time during based on service standard duration.
            # Ensures visit is at least 10 minutes long.
            visit_duration = max(
            visit_duration = max(
                10,
                int(
                    np.random.normal(
                        service["StandardDurationMinutes"],
                        8,
                    )
                ),
            )

            # Generates satisfaction score based on wait time and adds some random variation.
            # Keeps the final score between 1 and 5.
            satisfaction_score = int(
            satisfaction_score = int(
                np.clip(
                    round(
                        5.1
                        - max(wait_time, 0) / 25
                        + np.random.normal(0, 0.7)
                    ),
                    1,
                    5,
                )
            )

        # If appointment status is not Complete.
        else:
            actual_minutes = None
            visit_duration = None
            satisfaction_score = None

        # Creates appointment information. 
        appointment = {
            "AppointmentID": (
                f"A{first_appointment_number + row_number:06d}"
            ),
            "PatientID": random.choice(patient_ids),
            "ProviderID": provider_id,
            "ServiceID": service["ServiceID"],
            "ClinicID": random.choice(clinic_ids),
            "DepartmentID": department_id,
            "AppointmentDate": appointment_date.isoformat(),
            "ScheduledStartTime": minutes_to_time_text(
                scheduled_minutes
            ),
            "ActualStartTime": (
                minutes_to_time_text(actual_minutes)
                if actual_minutes is not None
                else None
            ),
            "AppointmentStatus": appointment_status,
            "BookingDate": booking_date.isoformat(),
            "VisitDurationMinutes": visit_duration,
            "SatisfactionScore": satisfaction_score,
            "PaymentMethod": random.choices(
                [
                    "Commercial Insurance",
                    "Medicare",
                    "Medicaid",
                    "Self-Pay",
                ],
                weights=[52, 20, 20, 8],
                k=1,
            )[0],
        }

        appointment_list.append(appointment)

    appointments = pd.DataFrame(appointment_list)

    # ========================================================================
    # INTENTIONAL DATA-QUALITY PROBLEMS
    # ========================================================================

    # Changes some Completed values so the spelling is inconsistent.
    completed_rows = appointments[
        appointments["AppointmentStatus"] == "Completed"
    ].index.tolist()

    if len(completed_rows) >= 9:
        appointments.loc[
            completed_rows[0:3],
            "AppointmentStatus",
        ] = "completed"

        appointments.loc[
            completed_rows[3:6],
            "AppointmentStatus",
        ] = "COMPLETE"

        appointments.loc[
            completed_rows[6:9],
            "AppointmentStatus",
        ] = "Completed "

    # Adds extra spaces to a few IDs.
    appointments.loc[5, "PatientID"] = (
        " " + str(appointments.loc[5, "PatientID"])
    )

    appointments.loc[12, "ClinicID"] = (
        str(appointments.loc[12, "ClinicID"]) + " "
    )

    # Uses a different date format in a few rows.
    for row_index in [20, 40, 60]:
        original_date = pd.to_datetime(
            appointments.loc[row_index, "AppointmentDate"]
        )
        appointments.loc[row_index, "AppointmentDate"] = (
            original_date.strftime("%m/%d/%Y")
        )

    return appointments

# ========================================================================
# PART 12: SAVE ALL OF THE FILES
# ========================================================================

def main():
    
    # Runs every step and saves every dataset.

    print("Creating fake healthcare data...")

    # Creates the tables.
    patients = create_patients()
    providers = create_providers()
    clinics = create_clinics()
    services = create_services()
    budgets = create_department_budget()

    # Saves patient table as Excel.
    patients.to_excel(
        OUTPUT_FOLDER / "patients.xlsx",
        index=False,
        engine="openpyxl",
    )

    # Saves provider table as CSV.
    providers.to_csv(
        OUTPUT_FOLDER / "providers.csv",
        index=False,
    )

    # Saves service table as CSV.
    services.to_csv(
        OUTPUT_FOLDER / "services.csv",
        index=False,
    )

    # Saves budget table as Excel.
    budgets.to_excel(
        OUTPUT_FOLDER / "department_budget.xlsx",
        index=False,
        engine="openpyxl",
    )

    # Saves clinic table as JSON. Each clinic becomes one JSON object.
    clinics.to_json(
        OUTPUT_FOLDER / "clinics.json",
        orient="records",
        indent=2,
    )

    # Creates three monthly appointment files.
    next_appointment_number = 100001

    for year, month in [
        (2026, 1),
        (2026, 2),
        (2026, 3),
    ]:

        # Creates appointment data for the current month. 
        appointments = create_appointments_for_month(
            year=year,
            month=month,
            patients=patients,
            providers=providers,
            services=services,
            first_appointment_number=next_appointment_number,
        )

        # Creates output file name for the current month.
        file_name = (
            f"appointments_{year}_{month:02d}.csv"
        )

        # Saves appointment data as a CSV file.
        appointments.to_csv(
            OUTPUT_FOLDER / file_name,
            index=False,
        )

        # Ensures next month AppointmentIDs continue after the current month.
        next_appointment_number += len(appointments)

    # Tells where the finished files were created.
    print()
    print("Finished!")
    print(f"Your files were created here: {OUTPUT_FOLDER}")
    print()

    # Prints every created file name.
    for file_path in sorted(OUTPUT_FOLDER.iterdir()):
        print(f"- {file_path.name}")

# ========================================================================
# PART 13: START THE SCRIPT
# ========================================================================

# Tells Python to run the main function when this file runs.
if __name__ == "__main__":
    main()