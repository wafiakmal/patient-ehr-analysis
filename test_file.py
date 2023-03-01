from typing import List, Tuple, Dict
import pytest
from patient_analysis import patient_is_sick
from patient_analysis import patient_age
from patient_analysis import parse_data
from patient_analysis import process_file
from fake_files import fake_files
from fake_files import write_file

PatientRecord = Dict[str, str]
PatientRecords = Tuple[List[PatientRecord], List[PatientRecord]]


def test_parse_data() -> None:
    with fake_files(
        [
            ["PatientID", "PatientName"],
            ["1", "Alice"],
            ["2", "Bob"],
        ],
        [
            ["PatientID", "LabName", "LabValue"],
            ["1", "Blood sugar", "100"],
            ["1", "Blood sugar", "110"],
            ["1", "Blood pressure", "120/80"],
            ["2", "Blood sugar", "90"],
        ],
    ) as (patient_file, lab_file):
        result = parse_data(patient_file, lab_file)
        assert result == (
            [
                {"PatientID": "1", "PatientName": "Alice"},
                {"PatientID": "2", "PatientName": "Bob"},
            ],
            [
                {
                    "PatientID": "1",
                    "LabName": "Blood sugar",
                    "LabValue": "100",
                },
                {
                    "PatientID": "1",
                    "LabName": "Blood sugar",
                    "LabValue": "110",
                },
                {
                    "PatientID": "1",
                    "LabName": "Blood pressure",
                    "LabValue": "120/80",
                },
                {"PatientID": "2", "LabName": "Blood sugar", "LabValue": "90"},
            ],
        )


def test_patient_age() -> None:
    records = (
        [
            {
                "PatientID": "1",
                "PatientName": "Alice",
                "PatientDateOfBirth": "1990-01-01 00:00:00.000",
            },
            {
                "PatientID": "2",
                "PatientName": "Bob",
                "PatientDateOfBirth": "1995-06-15 00:00:00.000",
            },
        ],
        [
            {"PatientID": "1", "LabName": "Blood sugar", "LabValue": "100"},
            {"PatientID": "1", "LabName": "Blood sugar", "LabValue": "110"},
            {
                "PatientID": "1",
                "LabName": "Blood pressure",
                "LabValue": "120/80",
            },
            {"PatientID": "2", "LabName": "Blood sugar", "LabValue": "90"},
        ],
    )
    patient_id = "1"
    result = patient_age(records, patient_id)
    assert result == 33


def test_patient_is_sick() -> None:
    lab_results = (
        [
            {"PatientID": "1", "PatientName": "Alice"},
        ],
        [
            {
                "PatientID": "1",
                "LabName": "METABOLIC: ALBUMIN",
                "LabValue": "100",
            },
            {
                "PatientID": "1",
                "LabName": "METABOLIC: ALBUMIN",
                "LabValue": "110",
            },
            {
                "PatientID": "1",
                "LabName": "Blood pressure",
                "LabValue": "120/80",
            },
        ],
    )
    patient_id = "1"
    lab_name = "METABOLIC: ALBUMIN"
    operator = ">"
    value = 105
    result = patient_is_sick(
        lab_results, patient_id, lab_name, operator, value
    )
    assert result


def test_patient_is_not_sick() -> None:
    lab_results = (
        [
            {"PatientID": "1", "PatientName": "Alice"},
        ],
        [
            {
                "PatientID": "1",
                "LabName": "METABOLIC: ALBUMIN",
                "LabValue": "100",
            },
            {
                "PatientID": "1",
                "LabName": "METABOLIC: ALBUMIN",
                "LabValue": "110",
            },
            {
                "PatientID": "1",
                "LabName": "Blood pressure",
                "LabValue": "120/80",
            },
        ],
    )
    patient_id = "1"
    lab_name = "METABOLIC: ALBUMIN"
    operator = "<"
    value = 130
    result = patient_is_sick(
        lab_results, patient_id, lab_name, operator, value
    )
    assert not result


def test_patient_not_exist() -> None:
    lab_results = (
        [
            {"PatientID": "1", "PatientName": "Alice"},
        ],
        [
            {
                "PatientID": "1",
                "LabName": "METABOLIC: ALBUMIN",
                "LabValue": "100",
            },
            {
                "PatientID": "1",
                "LabName": "METABOLIC: ALBUMIN",
                "LabValue": "110",
            },
            {
                "PatientID": "1",
                "LabName": "Blood pressure",
                "LabValue": "120/80",
            },
        ],
    )
    patient_id = "2"
    lab_name = "METABOLIC: ALBUMIN"
    operator = ">"
    value = 115
    result = patient_is_sick(
        lab_results, patient_id, lab_name, operator, value
    )
    assert not result
