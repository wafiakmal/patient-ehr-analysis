"""Give an analysis of patient based on personal and lab results data."""
from datetime import datetime


def process_file(filepath: str) -> list[dict[str, str]]:
    """
    Produce a list for versatile use of any txt format file.

    filepath: file path

    O(N**2) total
    """
    hold_data = []  # O(1)
    with open(filepath, encoding="utf-8-sig") as f:  # N times
        header = f.readline().strip().split("\t")  # O(1)
        for line in f:  # N times
            values = line.strip().split("\t")  # O(1)
            row = dict(zip(header, values))  # O(1)
            hold_data.append(row)  # O(1)
    return hold_data  # O(1)


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[list[dict[str, str]], ...]:
    """
    Make a tuple consisting patient personal file and lab results.

    Return a tuple containing two lists of dictionaries,
    Each dictionary will contain the data for one patient or lab result,
    The data expected to be delimited by tab, not any other type of delimiter.

    patient_filename: file containing the patient data, txt format
    lab_filename: the name of the file containing the lab data, txt format

    O(1) total
    """
    return process_file(patient_filename), process_file(lab_filename)  # O(1)


def patient_age(
    records: tuple[list[dict[str, str]], list[dict[str, str]]], patient_id: str
) -> int:
    """
    Give the year describing patient's age.

    Return the age of the patient with the given patient_id.
    records: the list of dictionaries containing the patient data, list format
    patient_id: the id of the patient, string format

    O(N**2) total
    """
    day_now = datetime.today()  # O(1)
    patient_age = 0  # O(1)
    for patient in records[0]:  # N times
        if patient["PatientID"] == patient_id:  # N times
            day_patient = datetime.strptime(
                patient["PatientDateOfBirth"], "%Y-%m-%d %H:%M:%S.%f"
            )  # O(1)
            patient_age = int((day_now - day_patient).days / 365.25)  # O(1)
    return patient_age  # O(1)


def patient_is_sick(
    records: tuple[list[dict[str, str]], list[dict[str, str]]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """
    Give a boolean value describing patient sick status.

    Return True if the patient with the given patient_id
    has lab value that is greater than or less than the given value.
    records: list of dictionaries containing lab data from parse_data function
    patient_id: the id of the patient, string format
    lab_name: the name of the lab test, string format
    operator: the operator to use in the comparison, string format
    value: the value to compare the lab value, float format

    O(N**3) total
    """
    for lab in records[1][:-1]:  # N times
        if (
            (lab["PatientID"] == patient_id)
            and (lab["LabName"] == lab_name)
            and (operator == ">")
            and (value < float(lab["LabValue"]))
        ):  # N times
            return True  # O(1)
        elif (
            (lab["PatientID"] == patient_id)
            and (lab["LabName"] == lab_name)
            and (operator == "<")
            and (value > float(lab["LabValue"]))
        ):  # N times
            return True  # O(1)
    return False  # O(1)


# For improvement, I think I need to make a line of code to ensure \
# the input are lowercase, certain format, and probably try to apply\
# recursion for lab data.
