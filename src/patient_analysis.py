"""Give an analysis of patient based on personal and lab results data."""
from datetime import datetime


class Lab:
    """Lab class for lab results."""

    def __init__(
        self,
        p_id: str,
        lab_name: str,
        lab_value: str,
        lab_date: str,
    ) -> None:
        """Initialize lab results."""
        self.patient_id = p_id
        self.name = lab_name
        self.value = float(lab_value)
        self.date = datetime.strptime(lab_date, "%Y-%m-%d %H:%M:%S.%f")


class Patient:
    """Patient class for patient personal file."""

    def __init__(
        self, id: str, gender: str, dob: str, marital: str, labs: list[Lab]
    ) -> None:
        """Initialize patient personal file."""
        self.id = id
        self.gender = gender
        self.dob = datetime.strptime(dob, "%Y-%m-%d %H:%M:%S.%f")
        self.marital = marital
        self.labs = labs

    @property
    def age(self) -> int:
        """Return the age of the patient."""
        today = datetime.today()
        return int((today - self.dob).days / 365.25)

    @property
    def age_first_test(self) -> int:
        """Return the age of the patient at first test."""
        all_dates = []
        for i in range(len(self.labs)):
            all_dates.append(self.labs[i].date)
        early_age = min(all_dates) - self.dob
        return int(early_age.days / 365.25)

    def is_sick(
        self, labname_in: str, operator_in: str, value_in: float
    ) -> bool:
        """Return whether the patient is sick."""
        for lab in self.labs:
            if lab.name == labname_in:
                if operator_in == ">":
                    if lab.value > value_in:
                        return True
                elif operator_in == "<":
                    if lab.value < value_in:
                        return True
        return False


def parse_data(patient_file: str, lab_file: str) -> dict[str, Patient]:
    """
    Produce a dictionary for patient personal file and lab results.

    Parameter
    ---------
    patient_file: str
        Location of the file containing the patient personal file, txt format.
    lab_file: str
        Location of the file containing the lab results, txt format.

    Variables:
    patient rows (MP) : lines in the patient personal file
        Rows containing patient data unique to each "PatientID".
    patient columns (NP) : columns in the patient personal file
        Columns containing patient personal file data.
    lab rows (ML) : lines in the lab results file
        Rows containing lab results unique to each "PatientID".
    lab columns (NL) : columns in the lab results file
        Columns containing lab results data.

    Return
    ------
    hold_patient: dict
        Dictionary containing patient personal file and lab results.

    Time complexity analysis:

        Lab data:
        hold_lab is created for holding lab data O(1).
        The file in lab_file is opened with utf-8-sig encoding O(1).
        The header is created O(NL).
        For loop of each line in the file O(ML).
        Each line is split into a list O(NL).
        The patient id is created O(1).
        The lab info is created by zipping header and values O(NL).
        A lab object is created O(1).
        If the patient id is not in the dictionary, the patient id is added
            as a key and the lab object is added as a value O(1).
        If the patient id is in the dictionary, the lab object is added as a
            value O(1).

        Patient data:
        hold_patient is created for holding patient personal file data O(1).
        The file in patient_file is opened with utf-8-sig encoding O(1).
        The header is created O(NP).
        For loop of each line in the file O(MP).
        Each line is split into a list O(NP).
        The patient id is created O(1).
        The patient info is created by zipping header and values O(NP).
        A patient object is created O(1).
        The patient id is added as a key and the patient object is added as a
            value O(1).

        This function complexity will scale according to the number of columns
            and rows of lab data O(NL*ML) and patient personal data O(NP*MP).
    """
    hold_lab: dict[str, list[Lab]] = dict()  # O(1)
    with open(lab_file, encoding="utf-8-sig") as f:  # O(1)
        header = f.readline().strip().split("\t")  # O(NL)
        for line in f:  # O(ML)
            values = line.strip("\n").split("\t")  # O(NL)
            patient_id = values[0]  # O(1)
            lab_info = dict(zip(header[1:], values[1:]))  # O(NL
            lab_object = Lab(
                patient_id,
                lab_info["LabName"],
                lab_info["LabValue"],
                lab_info["LabDateTime"],
            )  # O(1)
            if patient_id not in hold_lab:  # O(1)
                hold_lab[patient_id] = []  # O(1)
                hold_lab[patient_id].append(lab_object)  # O(1)
            else:  # O(1)
                hold_lab[patient_id].append(lab_object)  # O(1)
    hold_patient = dict()  # O(1)
    with open(patient_file, encoding="utf-8-sig") as f:  # O(1)
        header = f.readline().strip().split("\t")  # O(NP)
        for line in f:  # O(MP)
            values = line.strip("\n").split("\t")  # O(NP)
            patient_id = values[0]  # O(1)
            patient_info = dict(zip(header[1:], values[1:]))  # O(NP)
            patient_object = Patient(
                patient_id,
                patient_info["PatientGender"],
                patient_info["PatientDateOfBirth"],
                patient_info["PatientMaritalStatus"],
                hold_lab[patient_id],
            )  # O(1)
            hold_patient[patient_id] = patient_object  # O(1)
    return hold_patient  # O(1)
