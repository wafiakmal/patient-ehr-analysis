"""Patient analysis trial."""
import sqlite3
from datetime import datetime


class Lab:
    """Lab class for lab results."""

    def __init__(
        self,
        patient_id: str,
    ) -> None:
        """Initialize lab results."""
        connection = sqlite3.connect("ehr_data.db")
        c = connection.cursor()
        self.c = c
        self.p_id = patient_id


class Patient:
    """Patient class for patient personal file."""

    def __init__(self, patient_id: str) -> None:
        """Initialize patient personal file."""
        connection = sqlite3.connect("ehr_data.db")
        self.c = connection.cursor()
        self.p_id = patient_id

    @property
    def gender(self) -> str:
        """Return the gender of the patient."""
        cmd = f"SELECT gender FROM Patients WHERE patient_id = '{self.p_id}'"
        genderz = self.c.execute(cmd).fetchone()[0]
        return f"{genderz}"

    @property
    def dob(self) -> datetime:
        """Return the date of birth of the patient."""
        command = f"SELECT dob FROM Patients WHERE patient_id = '{self.p_id}'"
        self.c.execute(command)
        dobx = self.c.fetchone()[0]
        return datetime.strptime(dobx, "%Y-%m-%d %H:%M:%S.%f")

    @property
    def age(self) -> int:
        """Return the age of the patient."""
        today = datetime.today()
        return int((today - self.dob).days / 365.25)

    @property
    def age_first_test(self) -> int:
        """Return the age of the patient at first test."""
        command = (
            f"SELECT lab_date FROM Labs "
            f"WHERE patient_id = '{self.p_id}' ORDER BY lab_date"
        )
        self.f_lab = self.c.execute(command).fetchone()
        first_lab = datetime.strptime(self.f_lab[0], "%Y-%m-%d %H:%M:%S.%f")
        return int((first_lab - self.dob).days / 365.25)

    def is_sick(self, labname: str, operator: str, value: float) -> bool:
        """Return whether the patient is sick."""
        if operator == ">":
            command = (
                f"SELECT lab_value FROM Labs "
                f"WHERE patient_id = '{self.p_id}' "
                f"AND lab_name = '{labname}' "
                f"ORDER BY lab_value DESC"
            )
            high = self.c.execute(command).fetchone()
            if high[0] > value:
                return True
        elif operator == "<":
            command = (
                f"SELECT lab_value FROM Labs "
                f"WHERE patient_id = '{self.p_id}' "
                f"AND lab_name = '{labname}' "
                f"ORDER BY lab_value ASC"
            )
            low = self.c.execute(command).fetchone()
            if low[0] < value:
                self.c.close()
                return True


def parse_data(patient_file: str, lab_file: str) -> str:
    """Parse the patient and lab files."""
    conn = sqlite3.connect("ehr_data.db")
    c = conn.cursor()
    c.execute(
        f"SELECT name FROM sqlite_master WHERE "
        f"type='table' AND name='Patients' OR name='Labs'"
    )
    tables_check = c.fetchone()
    if tables_check is not None:
        c.execute(f"DROP TABLE Patients")
        c.execute(f"DROP TABLE Labs")
    c.execute(
        f"CREATE TABLE IF NOT EXISTS Patients(patient_id "
        f"VARCHAR PRIMARY KEY, gender VARCHAR, dob DATETIME, "
        f"race VARCHAR, marital VARCHAR, language VARCHAR, "
        f"poverty VARCHAR)"
    )
    c.execute(
        f"CREATE TABLE IF NOT EXISTS Labs(patient_id VARCHAR, "
        f"admissionID VARCHAR, lab_name VARCHAR, lab_value REAL, "
        f"lab_units VARCHAR, lab_date DATETIME)"
    )
    with open(lab_file, encoding="utf-8") as f:
        header = f.readline().strip().split("\t")
        for line in f:
            values = line.strip().split("\t")
            patient_id = values[0]
            lab_info = dict(zip(header, values))
            c.execute(
                f"INSERT INTO Labs VALUES(?,?,?,?,?,?)",
                (
                    patient_id,
                    lab_info["AdmissionID"],
                    lab_info["LabName"],
                    lab_info["LabValue"],
                    lab_info["LabUnits"],
                    lab_info["LabDateTime"],
                ),
            )
    with open(patient_file, encoding="utf-8") as f:
        header = f.readline().strip().split("\t")
        for line in f:
            values = line.strip().split("\t")
            patient_id = values[0]
            patient_info = dict(zip(header, values))
            c.execute(
                f"INSERT INTO Patients VALUES(?,?,?,?,?,?,?)",
                (
                    patient_id,
                    patient_info["PatientGender"],
                    patient_info["PatientDateOfBirth"],
                    patient_info["PatientRace"],
                    patient_info["PatientMaritalStatus"],
                    patient_info["PatientLanguage"],
                    patient_info["PatientPopulationPercentageBelowPoverty"],
                ),
            )
    conn.commit()
    conn.close()
    return f"Data parsed successfully to SQL database."
