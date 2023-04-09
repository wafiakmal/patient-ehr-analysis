from typing import List, Tuple, Dict
from datetime import datetime
import pytest
from patient_analysis import parse_data, Lab, Patient
from fake_files import fake_files


def test_parse_data() -> None:
    with fake_files(
        [
            [
                "PatientID",
                "PatientGender",
                "PatientDateOfBirth",
                "PatientRace",
                "PatientMaritalStatus",
                "PatientLanguage",
                "PatientPopulationPercentageBelowPoverty",
            ],
            [
                "1",
                "Male",
                "1973-08-16 10:58:34.413",
                "White",
                "Married",
                "English",
                "10",
            ],
            [
                "2",
                "Female",
                "1952-01-18 19:51:12.917",
                "Asian",
                "Single",
                "English",
                "20",
            ],
        ],
        [
            [
                "PatientID",
                "AdmissionID",
                "LabName",
                "LabValue",
                "LabUnits",
                "LabDateTime",
            ],
            [
                "1",
                "13",
                "METABOLIC: ALBUMIN",
                "100",
                "k/cumm",
                "2019-01-01 10:58:34.413",
            ],
            [
                "1",
                "1",
                "METABOLIC: ALBUMIN",
                "110",
                "k/cumm",
                "1992-06-27 03:32:50.653",
            ],
            [
                "2",
                "2",
                "METABOLIC: ALBUMIN",
                "90",
                "k/cumm",
                "2019-05-03 05:48:55.413",
            ],
        ],
    ) as (patient_file, lab_file):
        result = parse_data(patient_file, lab_file)
        assert result == "Data parsed successfully to SQL database."


def test_all_about_patient_class() -> None:
    assert Patient("1").age == 49
    assert Patient("1").age_first_test == 18
    assert Patient("2").gender == "Female"
    assert Patient("1").is_sick("METABOLIC: ALBUMIN", ">", 100.5)
    assert Patient("1").is_sick("METABOLIC: ALBUMIN", "<", 200.5)
    assert Patient("1").is_sick("CBC: MCHC", ">", 38.5) is False
