"""Give an analysis of patient based on personal and lab results data."""
from datetime import datetime


def base_data(filepath: str) -> dict[str, dict[str, str]]:
    """
    Produce a dictionary for patient base data.

    Parameter
    ---------
    filepath: str
        Location of the file containing the patient personal file, txt format.

    Variables:
    patient rows (A) : lines in the patient base data file
        Rows containing patient data unique to each "PatientID".
    patient columns (B) : columns in the patient base data file
        Columns of "PatientID", "PatientGender", "PatientDateOfBirth",
            "PatientRace", "PatientMaritalStatus", "PatientLanguage",
            "PatientPopulationPercentageBelowPoverty".
    header: first line of the file
        Contains the column names.
    values: each line in the file
        Contains the values for each column.

    Return
    ------
    hold_data: dict
        Dictionary containing patient personal file.

    Time complexity analysis:
    hold_data is created for holding data O(1) time complexity.
    The file in filepath is opened with utf-8-sig encoding O(1) time.
    Header created from splitting the first line in (A) by tab O(MP) time.
    Loop through each (A) with O(NP) time complexity.
    Values created from splitting (B) by tab with O(MP) time complexity.
    The PatientID is extracted from the values O(1) time complexity.
    The row is created by zipping the header and values O(1) time complexity.
    The row is added to the dictionary with PatientID as key O(1) time.
    Return hold_data with O(1) time complexity.
    Overall time complexity is O(NP*MP).

    Function will scale linearly with the number of (A) and (B) in the file,
        which is O(NP*MP).
    """
    hold_data = dict()  # O(1)
    with open(filepath, encoding="utf-8-sig") as f:  # O(1)
        header = f.readline().strip().split("\t")  # O(MP)
        for line in f:  # O(NP)
            values = line.strip().split("\t")  # O(MP)
            patient_id = values[0]  # O(1)
            row = dict(zip(header[1:], values[1:]))  # O(1)
            hold_data[patient_id] = row  # O(1)
    return hold_data  # O(1)


def records_data(filepath: str) -> dict[str, list[dict[str, str]]]:
    """
    Produce a dictionary for patient lab records.

    Parameter
    ---------
    filepath: str
        Location of the file containing the lab results, txt format.

    Variables:
    lab rows (C) : lines in the lab file
        Rows containing lab records unique to each "PatientID".
    lab columns (D) : columns in the lab file
        Columns containing "PatientID", "AdmissionID", "LabName", "LabValue",
            "LabUnits", "LabDateTime".
    header: first line of the file
        Contains the column names.
    values: each line in the file
        Contains the values for each column.

    Return
    ------
    hold_data: dict
        Dictionary containing lab records of each patient.

    Time complexity analysis:
    hold_data is created for holding data O(1) time complexity.
    The file in filepath is opened with utf-8-sig encoding O(1) time.
    Header created from splitting the first line in (C) by tab O(ML) time.
    Loop through each (C) with O(NL) time complexity.
    Values created from splitting (D) by tab with O(ML) time complexity.
    The PatientID is extracted from the values O(1) time complexity.
    The row is created by zipping the header and values O(1) time complexity.
    The row is added to the dictionary with PatientID as key O(1) time.
    Return hold_data with O(1) time complexity.
    Overall time complexity is O(NL*ML).

    Function will scale linearly with the number of (C) and (D) in the file,
        which is O(NL*ML).
    """
    holds_data: dict[str, list[dict[str, str]]] = dict()  # O(1)
    with open(filepath, encoding="utf-8-sig") as f:  # O(1)
        header = f.readline().strip().split("\t")  # O(ML)
        for line in f:  # O(NL)
            values = line.strip().split("\t")  # O(ML)
            patient_id = values[0]  # O(1)
            row = dict(zip(header[1:], values[1:]))  # O(1)
            if patient_id not in holds_data:  # O(1)
                holds_data[patient_id] = []  # O(1)
                holds_data[patient_id].append(row)  # O(1)
            else:
                holds_data[patient_id].append(row)  # O(1)
    return holds_data  # O(1)


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]]:
    """
    Make a tuple consisting patient personal file and lab results.

    Parameter
    ---------
    patient_filename: str
        Location of the file containing the patient personal file, txt format.
    lab_filename: str
        Location of the file containing the lab results, txt format.

    Return
    ------
    tuple
        Tuple of patient personal file and lab results.

    Time complexity analysis:
    The function base_data and records_data is called O(1) time complexity.

    This function complexity will scale according to the base_data O(NP*MP)
        and records_data function which is O(NL*ML).
    """
    return base_data(patient_filename), records_data(lab_filename)  # O(1)


def patient_age(
    records: tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]],
    patient_id: str,
) -> int:
    """
    Give the patient's age in years.

    Parameter
    ---------
    records: tuple
        Tuple of patient personal file and lab results.

    Variables:
    day_now: datetime
        Current date.
    day_patient: datetime
        Patient's birth date.
    patient_age: integer
        Patient's age.
    patient row (E) : dictionary
        Dictionary containing patient personal file.
    patient column (F) : dictionary
        Dictionary inside patient row containing patient personal file.

    Return
    ------
    patient_age: int
        Patient's age.


    Time complexity analysis:
    day_now created to hold the current date with O(1) time complexity.
    day_patient created by seeking the value of PatientDateOfBirth in (F),
        based on matched PatientID in (E) with O(1) time.
    patient_age created by subtracting day_now with day_patient the
        patient's age with O(1) time.
    Return the patient's age with O(1) time.
    Overall, the time complexity is O(1).

    This function won't scale with the number of patients.
    """
    day_now = datetime.today()  # O(1)
    day_patient = datetime.strptime(
        records[0][patient_id]["PatientDateOfBirth"], "%Y-%m-%d %H:%M:%S.%f"
    )  # O(1)
    patient_age = int((day_now - day_patient).days / 365.25)  # O(1)
    return patient_age  # O(1)


def patient_is_sick(
    records: tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """
    Give a boolean value describing patient sick status.

    Parameter
    ---------
    records: tuple
        Tuple of patient personal file and lab results.
    patient_id: str
        Patient's id.
    lab_name: str
        Name of the lab test.
    operator: str
        Operator to use in the comparison.
    value: float
        Value to compare the lab value.

    Variables:
    record row (G) : dictionary
        Dictionary containing lab results.
    record column (H) : dictionary
        Dictionary inside record row containing lab results.

    Return
    ------
    boolean
        True if the patient is sick, False otherwise.

    Time complexity analysis:
    If statement is used to check if patient_id is in (G) with O(1) time.
    For loop is used to loop through the lab (G) for specific patient
      with O(NL) time.
    If statement is used to check if the input lab_name is the same with
        LabName in (H), then comparing input value with LabValue in (H) based
        on input operator, with O(1) time.
    Conditions:
        If the operator is ">" and the LabValue in (H) is greater than
            the input value, return True with O(1) time.
        If the operator is "<" and the LabValue in (H) is less than the
            input value, return True with O(1) time.
        Else if both conditions above is not matched, return False
            with O(1) time.
    Overall, the time complexity is O(NL).

    This function will scale linearly with the number of (G) and (H),
        which is O(NL).
    """
    if patient_id in records[1]:  # O(1)
        for record in records[1][patient_id]:  # O(NL)
            if (
                (record["LabName"] == lab_name)
                and (operator == ">")
                and (float(record["LabValue"]) > value)
            ):  # O(1)
                return True  # O(1)
            elif (
                (record["LabName"] == lab_name)
                and (operator == "<")
                and (float(record["LabValue"]) < value)
            ):  # O(1)
                return True  # O(1)
    return False  # O(1)
