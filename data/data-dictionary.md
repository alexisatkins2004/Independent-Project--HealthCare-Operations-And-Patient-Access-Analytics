# Data Dictionary

---

## Monthly Appointment Data Dictionary 

| Column | Type | Description |
|----------|----------|----------|
| AppointmentID | Text | Unique identifier for each appointment. |
| PatientID | Text | Unique identifier for the patient associated with the appointment. Links to Patients table. |
| ProviderID | Text | Unique identifier for the healthcare provider conducting the appointment. Links to Providers table. |
| ServiceID | Text | Unique identifier for the medical service provided during the appointment. Links to Services table. |
| ClinicID | Text | Unique identifier for the clinic where the appointment takes place. Links to Clinics table. |
| DepartmentID | Text | Unique identifier for the department responsible for the appointment. Links to Department Budget table. |
| AppointmentDate | Date | Date the appointment is scheduled to occur. |
| ScheduledStartTime | Time | Time the appointment is scheduled to start. |
| ActualStartTime | Time | Actual time the appointment began. |
| AppointmentStatus | Text | Status of the appointment. |
| BookingDate | Date | Date the patient scheduled the appointment. |
| VisitDurationMinutes | Whole Number | Length of the completed appointment in minutes. |
| SatisfactionScore | Whole Number | Patient satisfaction rating on a scale from 1 to 5. |
| PaymentMethod | Text | Method used to pay for the appointment. |

---

## Patient Data Dictionary 

| Column | Type | Description |
|----------|----------|----------|
| PatientID | Text | Unique identifier for each patient. |
| BirthYear | Whole Number | Year the patient was born. |
| Gender | Text | Patient's reported gender. |
| City | Text | City where the patient resides. |
| State | Text | State where the patient resides. |
| PostalCode | Text | Postal code where the patient resides. |
| InsuranceType | Text | Patient's primary insurance coverage. |
| RegistrationDate | Date | Date the patient first registered with the healthcare network. |

---

## Provider Data Dictionary 

| Column | Type | Description |
|----------|----------|----------|
| ProviderID | Text | Unique identifier for each healthcare provider. |
| ProviderName | Text | Full name of the healthcare provider. |
| Specialty | Text | Medical specialty or area of practice. |
| DepartmentID | Text | Unique identifier for the department the provider belongs to. Links to Department Budget table. |
| HireDate | Date | Date the provider joined the healthcare network. |
| EmploymentType | Text | Employment status of the provider. |
| WeeklyCapacityHours | Whole Number | Number of hours the provider is available for appointments each week. |

---

## Clinic Data Dictionary 

| Column | Type | Description |
|----------|----------|----------|
| ClinicID | Text | Unique identifier for each clinic. |
| ClinicName | Text | Name of the healthcare clinic. |
| City | Text | City where the clinic is located. |
| State | Text | State where the clinic is located. |
| Region | Text | Geographic region in which the clinic operates. |
| TreatmentRooms | Whole Number | Number of treatment rooms available at the clinic. |
| DailyAppointmentCapacity | Whole Number | Maximum number of appointments the clinic can accommodate in a typical day. |

---

## Service Data Dictionary 

| Column | Type | Description |
|----------|----------|----------|
| ServiceID | Text | Unique identifier for each healthcare service. |
| ServiceName | Text | Name of the medical service provided. |
| ServiceCategory | Text | Category or department the service belongs to. |
| StandardPrice | Decimal Number | Standard amount charged to patients for the service. |
| EstimatedCost | Decimal Number | Estimated internal cost of providing the service. |
| StandardDurationMinutes | Whole Number | Expected duration of the service in minutes. |

---

## Department Budget Data Dictionary 

| Column | Type | Description |
|----------|----------|----------|
| DepartmentID | Text | Unique identifier for each department. |
| Month | Text | Month the budget applies to. |
| Budget | Decimal Number | Budget allocated to the department for the specified month. |
