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
        self.patient_id = patient_id


class Patient:
    """Patient class for patient personal file."""

    def __init__(self, patient_id: str) -> None:
        """Initialize patient personal file."""
        connection = sqlite3.connect("ehr_data.db")
        self.c = connection.cursor()
        self.id = patient_id

    @property
    def gender(self) -> str:
        """Return the gender of the patient."""
        cmd = "SELECT gender FROM Patients WHERE patient_id = ?"
        self.c.execute(cmd, (self.id,))
        genderz = self.c.fetchone()[0]
        return f"{genderz}"

    @property
    def dob(self) -> datetime:
        """Return the date of birth of the patient."""
        cmd = "SELECT dob FROM Patients WHERE patient_id = ?"
        self.c.execute(cmd, (self.id,))
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
            "SELECT lab_date FROM Labs "
            "WHERE patient_id = ? ORDER BY lab_date"
        )
        self.f_lab = self.c.execute(command, (self.id,)).fetchone()
        first_lab = datetime.strptime(self.f_lab[0], "%Y-%m-%d %H:%M:%S.%f")
        return int((first_lab - self.dob).days / 365.25)

    def is_sick(self, labname: str, operator: str, value: float) -> bool:
        """Return whether the patient is sick."""
        if operator == ">":
            command = (
                "SELECT lab_value FROM Labs "
                "WHERE patient_id = ? "
                "AND lab_name = ? "
                "ORDER BY lab_value DESC"
            )
            high = self.c.execute(command, (self.id, labname)).fetchone()
            if high is not None and high[0] > value:
                return True
        elif operator == "<":
            command = (
                "SELECT lab_value FROM Labs "
                "WHERE patient_id = ? "
                "AND lab_name = ? "
                "ORDER BY lab_value ASC"
            )
            low = self.c.execute(command, (self.id, labname)).fetchone()
            if low is not None and low[0] < value:
                return True
        return False


def parse_data(patient_file: str, lab_file: str) -> str:
    """Parse the patient and lab files."""
    conn = sqlite3.connect("ehr_data.db")
    c = conn.cursor()
    c.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name='Patients' OR name='Labs'"
    )
    tables_check = c.fetchone()
    if tables_check is not None:
        c.execute("DROP TABLE Patients")
        c.execute("DROP TABLE Labs")
    c.execute(
        "CREATE TABLE IF NOT EXISTS Patients(patient_id VARCHAR PRIMARY KEY, "
        "gender VARCHAR, dob DATETIME, race VARCHAR, marital VARCHAR, "
        "language VARCHAR, poverty VARCHAR)"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS Labs(patient_id VARCHAR, "
        "admissionID VARCHAR, lab_name VARCHAR, lab_value REAL, "
        "lab_units VARCHAR, lab_date DATETIME)"
    )
    with open(lab_file, encoding="utf-8") as f:
        header = f.readline().strip().split("\t")
        for line in f:
            values = line.strip().split("\t")
            patient_id = values[0]
            lab_info = dict(zip(header, values))
            c.execute(
                "INSERT INTO Labs VALUES(?,?,?,?,?,?)",
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
                "INSERT INTO Patients VALUES(?,?,?,?,?,?,?)",
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
    return "Data parsed successfully to SQL database."
