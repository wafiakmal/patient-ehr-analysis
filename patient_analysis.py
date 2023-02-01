from datetime import datetime


def parse_data(patient_filename: str, lab_filename: str, choose: str) -> list:
    """
    This function will read the patient and lab data from txt files and return a list of dictionaries,
    Each dictionary will contain the data for one patient or lab,
    Please Choose either "Patients" or "Lab" to specify the data you need,
    The data expected to be delimited by tab, not any other type of delimiter.
    patient_filename: the name of the file containing the patient data, in txt format
    lab_filename: the name of the file containing the lab data, in txt format
    choose: the data you need, either "Patients" or "Lab"
    """
    patients_data = []
    labs_data = []
    with open(patient_filename, encoding="utf-8-sig") as f:
        header = f.readline().strip().split("\t")
        for line in f:
            values = line.strip().split("\t")
            row = {}
            for i, value in enumerate(values):
                row[header[i]] = value
                pass
            patients_data.append(row)
            pass
        pass
    with open(lab_filename, encoding="utf-8-sig") as f:
        header = f.readline().strip().split("\t")
        for line in f:
            values = line.strip().split("\t")
            row = {}
            for i, value in enumerate(values):
                row[header[i]] = value
                pass
            labs_data.append(row)
            pass
        pass
    if choose == "Patients":
        return patients_data
    elif choose == "Lab":
        return labs_data
    else:
        return f'Please Choose Either "Patients" or "Lab" data'


def patient_age(records: list, patient_id: str) -> int:
    """
    This function will return the age of the patient with the given patient_id.
    records: the list of dictionaries containing the patient data, in list format
    patient_id: the id of the patient, in string format
    """
    for i in records:
        if i["PatientID"] == patient_id:
            pasien = datetime.strptime(
                i["PatientDateOfBirth"], "%Y-%m-%d %H:%M:%S.%f"
            )
            hari_ini = datetime.today()
            return int((hari_ini - pasien).days / 365.25)
        else:
            pass
        pass
    pass


def patient_is_sick(
    records: list, patient_id: str, lab_name: str, operator: str, value: float
):
    """
    This function will return True if the patient with the given patient_id has a lab value that is greater than the given value.
    records: the list of dictionaries containing the lab data, use the parse_data function to obtain this input
    patient_id: the id of the patient, in string format
    lab_name: the name of the lab test, in string format
    operator: the operator to use in the comparison, in string format
    value: the value to compare the lab value, in float format
    """
    i = 0
    while i < (len(records)):
        if (
            (records[i]["PatientID"] == patient_id)
            and (records[i]["LabName"] == lab_name)
            and (operator == ">")
            and (value < float(records[i]["LabValue"]))
        ):
            return True
        elif (
            (records[i]["PatientID"] == patient_id)
            and (records[i]["LabName"] == lab_name)
            and (operator == "<")
            and (value > float(records[i]["LabValue"]))
        ):
            return True
        else:
            i += 1
    return False


if __name__ == "__main__":
    records_patients = parse_data(
        "../ehr_files/PatientCorePopulatedTable.txt",
        "../ehr_files/LabsCorePopulatedTable.txt",
        "Patients",
    )
    records_lab = parse_data(
        "../ehr_files/PatientCorePopulatedTable.txt",
        "../ehr_files/LabsCorePopulatedTable.txt",
        "Lab",
    )
    print(
        patient_age(records_patients, "1A8791E3-A61C-455A-8DEE-763EB90C9B2C")
    )
    print(
        patient_is_sick(
            records_lab,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "METABOLIC: ALBUMIN",
            ">",
            4.0,
        )
    )
