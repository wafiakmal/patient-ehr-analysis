from typing import List, Tuple, Dict
from datetime import datetime
import pytest
from patient_analysis import parse_data
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
            ],
            [
                "1",
                "Male",
                "1973-08-16 10:58:34.413",
                "White",
                "Married",
            ],
            [
                "2",
                "Female",
                "1952-01-18 19:51:12.917",
                "Asian",
                "Single",
            ],
        ],
        [
            [
                "PatientID",
                "AdmissionID",
                "LabName",
                "LabValue",
                "LabUnits",
                "LabDate",
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
        patient1 = result["1"]
        assert patient1.p_id == "1"
        assert patient1.gender == "Male"
        assert patient1.dob == datetime.strptime(
            "1973-08-16 10:58:34.413", "%Y-%m-%d %H:%M:%S.%f"
        )
        assert patient1.marital == "Married"


def test_all_about_patient_class() -> None:
    with fake_files(
        [
            [
                "PatientID",
                "PatientGender",
                "PatientDateOfBirth",
                "PatientRace",
                "PatientMaritalStatus",
            ],
            [
                "1",
                "Male",
                "1973-08-16 10:58:34.413",
                "White",
                "Married",
            ],
            [
                "2",
                "Female",
                "1952-01-18 19:51:12.917",
                "Asian",
                "Single",
            ],
        ],
        [
            [
                "PatientID",
                "AdmissionID",
                "LabName",
                "LabValue",
                "LabUnits",
                "LabDate",
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
        assert result["1"].age == 49
        assert result["1"].age_first_test == 18
        assert result["1"].is_sick("METABOLIC: ALBUMIN", ">", 100.5)
        assert result["1"].is_sick("METABOLIC: ALBUMIN", "<", 200.5)
        assert result["2"].is_sick("CBC: MCHC", ">", 38.5) is False
