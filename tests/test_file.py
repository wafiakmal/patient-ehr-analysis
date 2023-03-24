from typing import List, Tuple, Dict
import pytest
from patient_analysis import patient_is_sick
from patient_analysis import patient_age
from patient_analysis import parse_data
from patient_analysis import age_first_test
from fake_files import fake_files


def test_parse_data() -> None:
    with fake_files(
        [
            ["PatientID", "PatientGender", "PatientDateOfBirth"],
            ["1", "Male", "1973-08-16 10:58:34.413"],
            ["2", "Female", "1952-01-18 19:51:12.917"],
        ],
        [
            ["PatientID", "LabName", "LabValue"],
            ["1", "METABOLIC: ALBUMIN", "100"],
            ["1", "METABOLIC: ALBUMIN", "110"],
            ["2", "METABOLIC: ALBUMIN", "90"],
        ],
    ) as (patient_file, lab_file):
        result = parse_data(patient_file, lab_file)
        assert result == (
            {
                "1": {
                    "PatientGender": "Male",
                    "PatientDateOfBirth": "1973-08-16 10:58:34.413",
                },
                "2": {
                    "PatientGender": "Female",
                    "PatientDateOfBirth": "1952-01-18 19:51:12.917",
                },
            },
            {
                "1": [
                    {"LabName": "METABOLIC: ALBUMIN", "LabValue": "100"},
                    {"LabName": "METABOLIC: ALBUMIN", "LabValue": "110"},
                ],
                "2": [{"LabName": "METABOLIC: ALBUMIN", "LabValue": "90"}],
            },
        )


def test_patient_age() -> None:
    records = (
        {
            "1": {
                "PatientGender": "Male",
                "PatientDateOfBirth": "1973-08-16 10:58:34.413",
            },
            "2": {
                "PatientGender": "Female",
                "PatientDateOfBirth": "1952-01-18 19:51:12.917",
            },
        },
        {
            "1": [
                {"LabName": "METABOLIC: ALBUMIN", "LabValue": "100"},
                {"LabName": "METABOLIC: ALBUMIN", "LabValue": "110"},
            ],
            "2": [{"LabName": "METABOLIC: ALBUMIN", "LabValue": "90"}],
        },
    )
    patient_id = "1"
    result = patient_age(records, patient_id)
    assert result == 49


def test_patient_is_sick() -> None:
    lab_results = (
        {
            "1": {
                "PatientGender": "Male",
                "PatientDateOfBirth": "1973-08-16 10:58:34.413",
            },
            "2": {
                "PatientGender": "Female",
                "PatientDateOfBirth": "1952-01-18 19:51:12.917",
            },
        },
        {
            "1": [
                {"LabName": "METABOLIC: ALBUMIN", "LabValue": "100"},
                {"LabName": "METABOLIC: ALBUMIN", "LabValue": "110"},
            ],
            "2": [{"LabName": "METABOLIC: ALBUMIN", "LabValue": "90"}],
        },
    )
    patient_id1 = "1"
    lab_name1 = "METABOLIC: ALBUMIN"
    operator1 = ">"
    value1 = 105
    result1 = patient_is_sick(
        lab_results, patient_id1, lab_name1, operator1, value1
    )
    assert result1
    patient_id2 = "1"
    lab_name2 = "METABOLIC: ALBUMIN"
    operator2 = "<"
    value2 = 130
    result2 = patient_is_sick(
        lab_results, patient_id2, lab_name2, operator2, value2
    )
    assert result2
    patient_id3 = "3"
    lab_name3 = "METABOLIC: ALBUMIN"
    operator3 = ">"
    value3 = 115
    result3 = patient_is_sick(
        lab_results, patient_id3, lab_name3, operator3, value3
    )
    assert result3 is False


def test_age_first_test() -> None:
    records = (
        {
            "1": {
                "PatientGender": "Male",
                "PatientDateOfBirth": "1973-08-16 10:58:34.413",
            },
            "2": {
                "PatientGender": "Female",
                "PatientDateOfBirth": "1952-01-18 19:51:12.917",
            },
        },
        {
            "1": [
                {
                    "LabName": "METABOLIC: ALBUMIN",
                    "LabValue": "100",
                    "LabDateTime": "2021-01-01 10:58:34.413",
                },
                {
                    "LabName": "METABOLIC: ALBUMIN",
                    "LabValue": "110",
                    "LabDateTime": "1992-06-27 03:32:50.653",
                },
            ],
            "2": [
                {
                    "LabName": "METABOLIC: ALBUMIN",
                    "LabValue": "90",
                    "LabDateTime": "2019-01-01 10:58:34.413",
                }
            ],
        },
    )
    patient_id = "1"
    result = age_first_test(records, patient_id)
    assert result == 18
