"""Give an analysis of patient based on personal and lab results data."""
from datetime import datetime


def process(
    filepath: str,
) -> dict[str, list[list[str]]]:
    """
    Produce a dictionary for any txt file with tab delimiter.

    filepath: file path
    hold_data: dictionary to hold data

    Time complexity analysis:
    hold_data is created for holding data O(1) time complexity.
    The file in filepath is opened with utf-8-sig encoding O(1) time.
    Loop through each line in the file O(N) time complexity.
    Values in each line is then split by tab O(M) time complexity.
    If key is not in the dictionary, create a key and append the value O(1).
    Elif key is in the dictionary, append the value O(1).
    Return hold_data with O(1) time complexity.
    Overall time complexity is O(N*M).

    Function will scale linearly with the number of lines and columns
        in the file, which is O(N*M).
    """
    hold_data: dict[str, list[list[str]]] = dict()  # O(1)
    with open(filepath, encoding="utf-8-sig") as f:  # O(1)
        for line in f:  # O(N)
            values = line.strip().split("\t")  # O(M)
            if values[0] not in hold_data:
                hold_data[values[0]] = []  # O(1)
                hold_data[values[0]].append(values[1:])  # O(1)
            else:
                hold_data[values[0]].append(values[1:])  # O(1)
    return hold_data  # O(1)


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[dict[str, list[list[str]]], ...]:
    """
    Make a tuple consisting patient personal file and lab results.

    Return a tuple containing two dictionaries,
    Each dictionary will contain the data for one patient or lab result,
    The data expected to be delimited by tab, not any other type of delimiter.

    patient_filename: file containing the patient data, txt format
    lab_filename: the name of the file containing the lab data, txt format

    Time complexity analysis:
    The function process_file is called twice with O(1) time complexity.
    The function process_file is called with O(N*M) time complexity.

    This function complexity will scale according to the process_file function
        which is O(N*M).
    """
    return process(patient_filename), process(lab_filename)  # O(N*M)


def patient_age(
    records: tuple[dict[str, list[list[str]]], ...], patient_id: str
) -> int:
    """
    Give the year describing patient's age.

    Return the age of the patient with the given patient_id.
    records: the dictionaries containing the patient data.
    patient_id: the id of the patient, string format.

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
        records[0][patient_id][0][1], "%Y-%m-%d %H:%M:%S.%f"
    )  # O(1)
    patient_age = int((day_now - day_patient).days / 365.25)  # O(1)
    return patient_age  # O(1)


def patient_is_sick(
    records: tuple[dict[str, list[list[str]]], ...],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """
    Give a boolean value describing patient sick status.

    Return True if the patient with the given patient_id
    has lab value that is greater than or less than the given value.
    records: dictionaries containing lab data from parse_data function
    patient_id: the id of the patient, string format
    lab_name: the name of the lab test, string format
    operator: the operator to use in the comparison, string format
    value: the value to compare the lab value, float format

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
                (record[1] == lab_name)
                and (operator == ">")
                and (value < float(record[2]))
            ):  # O(1)
                return True  # O(1)
            elif (
                (record[1] == lab_name)
                and (operator == "<")
                and (value > float(record[2]))
            ):  # O(1)
                return True  # O(1)
    return False  # O(1)
