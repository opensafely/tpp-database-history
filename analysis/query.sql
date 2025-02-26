DECLARE @from_date DATE;
SET @from_date = DATEFROMPARTS(2016, 1, 1);

DECLARE @to_date DATE;
SET @to_date = CONVERT(DATE, GETDATE());

SELECT
    'CodedEvent' AS table_name,
    CONVERT(DATE, ConsultationDate) AS event_date,
    COUNT(*) AS event_count
FROM CodedEvent
WHERE
    CONVERT(DATE, ConsultationDate) >= @from_date
    AND CONVERT(DATE, ConsultationDate) <= @to_date
    AND Patient_ID NOT IN (SELECT Patient_ID FROM PatientsWithTypeOneDissent)
GROUP BY CONVERT(DATE, ConsultationDate)

UNION ALL

SELECT
    'Appointment' AS table_name,
    CONVERT(DATE, SeenDate) AS event_date,
    COUNT(*) AS event_count
FROM Appointment
WHERE
    CONVERT(DATE, SeenDate) >= @from_date
    AND CONVERT(DATE, SeenDate) <= @to_date
    AND Patient_ID NOT IN (SELECT Patient_ID FROM PatientsWithTypeOneDissent)
GROUP BY CONVERT(DATE, SeenDate)

UNION ALL

SELECT
    'APCS' AS table_name,
    Admission_Date AS event_date,
    COUNT(*) AS event_count
FROM APCS
WHERE
    Admission_Date >= @from_date
    AND Admission_Date <= @to_date
    AND Patient_ID NOT IN (SELECT Patient_ID FROM PatientsWithTypeOneDissent)
GROUP BY Admission_Date

UNION ALL

SELECT
    'APCS_ARCHIVED' AS table_name,
    Admission_Date AS event_date,
    COUNT(*) AS event_count
FROM APCS_ARCHIVED
WHERE
    Admission_Date >= @from_date
    AND Admission_Date <= @to_date
    AND Patient_ID NOT IN (SELECT Patient_ID FROM PatientsWithTypeOneDissent)
GROUP BY Admission_Date

UNION ALL

SELECT
    'CPNS' AS table_name,
    DateOfDeath AS event_date,
    COUNT(*) AS event_count
FROM CPNS
WHERE
    DateOfDeath >= @from_date
    AND DateOfDeath <= @to_date
    AND Patient_ID NOT IN (SELECT Patient_ID FROM PatientsWithTypeOneDissent)
GROUP BY DateOfDeath

UNION ALL

SELECT
    'EC' AS table_name,
    Arrival_Date AS event_date,
    COUNT(*) AS event_count
FROM EC
WHERE
    Arrival_Date >= @from_date
    AND Arrival_Date <= @to_date
    AND Patient_ID NOT IN (SELECT Patient_ID FROM PatientsWithTypeOneDissent)
GROUP BY Arrival_Date

UNION ALL

SELECT
    'EC_ARCHIVED' AS table_name,
    Arrival_Date AS event_date,
    COUNT(*) AS event_count
FROM EC_ARCHIVED
WHERE
    Arrival_Date >= @from_date
    AND Arrival_Date <= @to_date
    AND Patient_ID NOT IN (SELECT Patient_ID FROM PatientsWithTypeOneDissent)
GROUP BY Arrival_Date

UNION ALL

SELECT
    'OPA' AS table_name,
    Appointment_Date AS event_date,
    COUNT(*) AS event_count
FROM OPA
WHERE
    Appointment_Date >= @from_date
    AND Appointment_Date <= @to_date
    AND Patient_ID NOT IN (SELECT Patient_ID FROM PatientsWithTypeOneDissent)
GROUP BY Appointment_Date

UNION ALL

SELECT
    'OPA_ARCHIVED' AS table_name,
    Appointment_Date AS event_date,
    COUNT(*) AS event_count
FROM OPA_ARCHIVED
WHERE
    Appointment_Date >= @from_date
    AND Appointment_Date <= @to_date
    AND Patient_ID NOT IN (SELECT Patient_ID FROM PatientsWithTypeOneDissent)
GROUP BY Appointment_Date

UNION ALL

SELECT
    'ICNARC' AS table_name,
    CONVERT(DATE, IcuAdmissionDateTime) AS event_date,
    COUNT(*) AS event_count
FROM ICNARC
WHERE
    CONVERT(DATE, IcuAdmissionDateTime) >= @from_date
    AND CONVERT(DATE, IcuAdmissionDateTime) <= @to_date
    AND Patient_ID NOT IN (SELECT Patient_ID FROM PatientsWithTypeOneDissent)
GROUP BY CONVERT(DATE, IcuAdmissionDateTime)

UNION ALL

SELECT
    'ONS_Deaths' AS table_name,
    dod AS event_date,
    COUNT(*) AS event_count
FROM ONS_Deaths
WHERE
    dod >= @from_date
    AND dod <= @to_date
    AND Patient_ID NOT IN (SELECT Patient_ID FROM PatientsWithTypeOneDissent)
GROUP BY dod

UNION ALL

SELECT
    'SGSS_Positive' AS table_name,
    Earliest_Specimen_Date AS event_date,
    COUNT(*) AS event_count
FROM SGSS_Positive
WHERE
    Earliest_Specimen_Date >= @from_date
    AND Earliest_Specimen_Date <= @to_date
    AND Patient_ID NOT IN (SELECT Patient_ID FROM PatientsWithTypeOneDissent)
GROUP BY Earliest_Specimen_Date

UNION ALL

SELECT
    'SGSS_Negative' AS table_name,
    Earliest_Specimen_Date AS event_date,
    COUNT(*) AS event_count
FROM SGSS_Negative
WHERE
    Earliest_Specimen_Date >= @from_date
    AND Earliest_Specimen_Date <= @to_date
    AND Patient_ID NOT IN (SELECT Patient_ID FROM PatientsWithTypeOneDissent)
GROUP BY Earliest_Specimen_Date

UNION ALL

SELECT
    'SGSS_AllTests_Positive' AS table_name,
    Specimen_Date AS event_date,
    COUNT(*) AS event_count
FROM SGSS_AllTests_Positive
WHERE
    Specimen_Date >= @from_date
    AND Specimen_Date <= @to_date
    AND Patient_ID NOT IN (SELECT Patient_ID FROM PatientsWithTypeOneDissent)
GROUP BY Specimen_Date

UNION ALL

SELECT
    'SGSS_AllTests_Negative' AS table_name,
    Specimen_Date AS event_date,
    COUNT(*) AS event_count
FROM SGSS_AllTests_Negative
WHERE
    Specimen_Date >= @from_date
    AND Specimen_Date <= @to_date
    AND Patient_ID NOT IN (SELECT Patient_ID FROM PatientsWithTypeOneDissent)
GROUP BY Specimen_Date

ORDER BY table_name, event_date, event_count
