"""Give an analysis of patient based on personal and lab results data."""
from datetime import datetime


def process_file(filepath: str) -> list[dict[str, str]]:
    """
    Produce a list for versatile use of any txt format file with tab delimiter.

    filepath: file path

    Time complexity analysis:
    An empty list is created for holding data O(1).
    The file based on filepath is opened with utf-8-sig encoding O(1).
    A key created for the header of the file with O(1) operation.
    Using for loop, each line in the file is read with N times.
    Creating a dictionary from the header row and data row with a linear time
    operation with respect to the number of columns in the file M times.
    The value added to dictionary is performed with 3 times O(1), for N times.
    The dictionary is then appended to a list O(1), which is returned O(1).
    Overall time complexity is O(N*M)

    Function will scale linearly with the number of lines and columns
    in file.
    """
    hold_data = []  # O(1)
    with open(filepath, encoding="utf-8-sig") as f:  # O(1)
        header = f.readline().strip().split("\t")  # O(1)
        for line in f:  # N times
            values = line.strip().split("\t")  # M times
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

    Time complexity analysis:
    The function process_file is called twice with O(1) time complexity.

    This function complexity will scale according to the process_file function
    which is O(N*M).
    """
    return process_file(patient_filename), process_file(lab_filename)  # O(1)


def patient_age(
    records: tuple[list[dict[str, str]], ...], patient_id: str
) -> int:
    """
    Give the year describing patient's age.

    Return the age of the patient with the given patient_id.
    records: the list of dictionaries containing the patient data, list format
    patient_id: the id of the patient, string format

    Time complexity analysis:
    A variable is created to hold the current date with O(1) time complexity.
    A dummy variable is created to hold the initial patient age with O(1) time.
    A for loop is created to iterate through the patient data with N times.
    An if statement to check if the patient id is the same with O(1) times.
    O(1) process done if the condition is met, replacing patient age with O(1).
    The patient age is returned with O(1) time complexity.
    Dropping the constant, the time complexity is O(N).

    This function will scale linearly with the number of patient records.
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
    records: tuple[list[dict[str, str]], ...],
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

    Time complexity analysis:
    A for loop is created to iterate through the lab data with N times.
    An if-elif statement is created to check if the patient id, lab name,
    operator, and value is the same with input O(1) times.
    Return True if the condition is met with O(1) time complexity.
    No placeholder is created for the else statement.
    Overall, the time complexity is O(N).

    This function will scale linearly with the number of lab records (N times).
    """
    for lab in records[1][:-1]:  # N times
        if (
            (lab["PatientID"] == patient_id)
            and (lab["LabName"] == lab_name)
            and (operator == ">")
            and (value < float(lab["LabValue"]))
        ):  # O(1)
            return True  # O(1)
        elif (
            (lab["PatientID"] == patient_id)
            and (lab["LabName"] == lab_name)
            and (operator == "<")
            and (value > float(lab["LabValue"]))
        ):  # O(1)
            return True  # O(1)
    return False  # O(1)
