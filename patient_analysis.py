"""Give an analysis of patient based on personal and lab results data."""
from datetime import datetime


def base_data(filepath: str) -> dict[str, dict[str, str]]:
    """
    Produce a dictionary for patient base data.

    Parameter
    ---------
    filepath: str
        Location of the file containing the patient personal file, txt format.

    Return
    ------
    hold_data: dict
        Dictionary containing patient personal file.

    Time complexity analysis:
    hold_data is created for holding data O(1) time complexity.
    The file in filepath is opened with utf-8-sig encoding O(1) time.
    The header is read and split by tab O(M) time complexity.
    Loop through each line in the file O(N) time complexity.
    Values in each line is then split by tab O(M) time complexity.
    The patient_id is extracted from the values O(1) time complexity.
    The row is created by zipping the header and values O(1) time complexity.
    The row is added to the dictionary with patient_id as key O(1) time.
    Return hold_data with O(1) time complexity.
    Overall time complexity is O(N*M).

    Function will scale linearly with the number of lines and columns
        in the file, which is O(N*M).
    """
    hold_data = dict()  # O(1)
    with open(filepath, encoding="utf-8-sig") as f:  # O(1)
        header = f.readline().strip().split("\t")  # O(M)
        for line in f:  # O(N)
            values = line.strip().split("\t")  # O(M)
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

    Return
    ------
    hold_data: dict
        Dictionary containing lab records of each patient.

    Time complexity analysis:
    hold_data is created for holding data O(1) time complexity.
    The file in filepath is opened with utf-8-sig encoding O(1) time.
    The header is read and split by tab O(M) time complexity.
    Loop through each line in the file O(N) time complexity.
    Values in each line is then split by tab O(M) time complexity.
    The patient_id is extracted from the values O(1) time complexity.
    The row is created by zipping the header and values O(1) time complexity.
    The row is added to the dictionary with patient_id as key O(1) time.
    Return hold_data with O(1) time complexity.
    Overall time complexity is O(N*M).

    Function will scale linearly with the number of lines and columns
        in the file, which is O(N*M).
    """
    holds_data: dict[str, list[dict[str, str]]] = dict()  # O(1)
    with open(filepath, encoding="utf-8-sig") as f:  # O(1)
        header = f.readline().strip().split("\t")  # O(M)
        for line in f:  # O(N)
            values = line.strip().split("\t")  # O(M)
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
    The function process_file is called twice with O(1) time complexity.
    The function process_file is called with O(N*M) time complexity.

    This function complexity will scale according to the process_file function
        which is O(N*M).
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

    Return
    ------
    patient_age: int
        Patient's age.


    Time complexity analysis:
    day_now created to hold the current date with O(1) time complexity.
    day_patient created to hold the patient's birth date with O(1) time.
    patient_age created to calculate the patient's age with O(1) time.
    Return the patient's age with O(1) time.
    Overall, the time complexity is O(1).

    IMO, This function won't scale with the number of patients.
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

    Return
    ------
    boolean
        True if the patient is sick, False otherwise.

    Time complexity analysis:
    If statement is used to check if patient_id is in records with O(1) time.
    For loop is used to loop through the lab records for specific patient
      with O(N) time.
    If statement is used to check if the lab_name is the same, then comparing
        operator and value, with O(1) time.
    Return True if the patient is sick with O(1) time.
    Return False if the patient is not sick with O(1) time.
    Overall, the time complexity is O(N).

    This function will scale linearly with the number of lab records,
        which is O(N).
    """
    if patient_id in records[1]:  # O(1)
        for record in records[1][patient_id]:  # O(N)
            if (
                (record["LabName"] == lab_name)
                and (operator == ">")
                and (value < float(record["LabValue"]))
            ):  # O(1)
                return True  # O(1)
            elif (
                (record["LabName"] == lab_name)
                and (operator == "<")
                and (value > float(record["LabValue"]))
            ):  # O(1)
                return True  # O(1)
    return False  # O(1)
