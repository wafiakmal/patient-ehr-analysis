"""Give an analysis of patient based on personal and lab results data."""


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """
    Make a tuple consisting patient personal file and lab results.

    Return a list of tuple containing a list filled with dictionaries,
    Each dictionary will contain the data for one patient or lab,
    Please Choose either "Patients" or "Lab" to specify the data you need,
    The data expected to be delimited by tab, not any other type of delimiter.

    patient_filename: file containing the patient data, txt format
    lab_filename: the name of the file containing the lab data, txt format
    choose: the data you need, either "Patients" or "Lab"
    """
    patients_data = []
    labs_data = []
    temp_list = [patient_filename, lab_filename]
    for i in range(len(temp_list)):
        with open(temp_list[i], encoding="utf-8-sig") as f:
            header = f.readline().strip().split("\t")
            for line in f:
                values = line.strip().split("\t")
                row = {}
                for j, value in enumerate(values):
                    row[header[j]] = value
                if temp_list[i] == patient_filename:
                    patients_data.append(row)
                else:
                    labs_data.append(row)
    return (patients_data, labs_data)


def patient_age(
    records: tuple[list[dict[str, str]], list[dict[str, str]]], patient_id: str
) -> int:
    """
    Give the year describing patient's age.

    Return the age of the patient with the given patient_id.
    records: the list of dictionaries containing the patient data, list format
    patient_id: the id of the patient, string format
    """
    from datetime import datetime

    patient_age = 0
    for i in records[0]:
        if i["PatientID"] == patient_id:
            pasien = datetime.strptime(
                i["PatientDateOfBirth"], "%Y-%m-%d %H:%M:%S.%f"
            )
            hari_ini = datetime.today()
            patient_age = int((hari_ini - pasien).days / 365.25)
    return patient_age


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
    has lab value that is greater than the given value.
    records: list of dictionaries containing lab data from parse_data function
    patient_id: the id of the patient, string format
    lab_name: the name of the lab test, string format
    operator: the operator to use in the comparison, string format
    value: the value to compare the lab value, float format
    """
    i = 0
    lab_list = records[1]
    while i < (len(lab_list) - 1):
        if (
            (lab_list[i]["PatientID"] == patient_id)
            and (lab_list[i]["LabName"] == lab_name)
            and (operator == ">")
            and (value < float(lab_list[i]["LabValue"]))
        ):
            return True
        elif (
            (lab_list[i]["PatientID"] == patient_id)
            and (lab_list[i]["LabName"] == lab_name)
            and (operator == "<")
            and (value > float(lab_list[i]["LabValue"]))
        ):
            return True
        else:
            i += 1
    return False


if __name__ == "__main__":
    records = parse_data(
        "../ehr_files/PatientCorePopulatedTable.txt",
        "../ehr_files/LabsCorePopulatedTable.txt",
    )
    print(patient_age(records, "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"))
    print(
        patient_is_sick(
            records,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "METABOLIC: ALBUMIN",
            ">",
            4.0,
        )
    )
