# ehr-utils

The ehr-utils library provides some simple analytical capabilities for EHR data.

# Note to end users:

## Input file formats:
This library takes two txt files as input. The first file contains patient base data and the second file contains patient lab data.

The details of the input file formats are described in the following sections.

### Patient base data file format:
The file is a tab delimited file with the following columns:
1. PatientID
2. PatientGender
3. PatientDateOfBirth
4. PatientRace
5. PatientMaritalStatus
6. PatientLanguage
7. PatientPopulationPercentageBelowPoverty

### Patient lab data file format:
The file is a tab delimited file with the following columns:
1. PatientID
2. LabName
3. LabValue
4. LabUnits
5. LabDateTime

All the values in both files are strings. This library will convert all the values to the appropriate data types.

## Using the library:
The library contains 3 helper functions to process the input files and 2 main functions to calculate patient age and to determine whether or not a patient is sick.

Example of using the library:

### To calculate patient's age, we use the `patient_age` function, general instruction for running the function:

```python
from patient_analysis import parse_data
from patient_analysis import patient_age

# parse the input files
records = parse_data('LOCATION OF YOUR PATIENT BASE DATA TXT FILE':str, 'LOCATION OF YOUR PATIENT LAB DATA TXT FILE':str)

# calculate patient's age
patient_age(records, patient_id:str)
```
For example, 

```python
patient_age(records, "1A8791E3-A61C-455A-8DEE-763EB90C9B2C")
```

will return an integer such as the following output:

```python
>>> 45
```

### To determine whether or not a patient is sick, we use the `patient_is_sick` function. should take the data and return a boolean indicating whether the patient has ever had a test with value above (">") or below ("<") the given level. Below is the general instructions of running the function:

```python
from patient_analysis import parse_data
from patient_analysis import patient_is_sick

# parse the input files
records = parse_data('LOCATION OF YOUR PATIENT BASE DATA TXT FILE':str, 'LOCATION OF YOUR PATIENT LAB DATA TXT FILE':str)

# determine whether or not a patient is sick
patient_is_sick(records, patient_id: str, lab_name: str, operator: str, value: float)
```

For example, 

```python
patient_is_sick(records, "1A8791E3-A61C-455A-8DEE-763EB90C9B2C", "METABOLIC: ALBUMIN", ">", 4.0)
```

will return a Boolean such as the following output:

```python
>>> True
```

# Note to contributors:

## Local testing instructions:
To run the tests locally, we included a test_files.py and fake_files.py, you only need to run the following commands in the terminal:

### Run the test
```
coverage run -m pytest test_file.py > test_report.txt
```

### Generate the coverage report
```
coverage report
```