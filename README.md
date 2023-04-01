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
The library is coded in Python. This library use object-oriented approach, with combination of classes and functions. Base and lab data are stored using two separate classes, but combined into one dictionary with by `parse_data` function and patient ID as the key.

Example of using the library:

### To calculate patient's age, we just need to call the `.age` property of `Patient` Class. The general instruction for running the function:

```python
from patient_analysis import parse_data

# parse the input files
patient = parse_data("LOCATION OF YOUR PATIENT BASE DATA TXT FILE":str, "LOCATION OF YOUR PATIENT LAB DATA TXT FILE":str)

# calculate patient's age
patient["ID OF THE PATIENT"].age
```
```
For example, 

```python
patient_age["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].age
```
```

will return an integer such as the following output:

```python
>>> 49
```

### To calculate patient's age when they record their first lab test result, we just need to call the `.age_first_test` property of `Patient` Class. The general instruction for running the function:

```python
from patient_analysis import parse_data

# parse the input files
patient = parse_data("LOCATION OF YOUR PATIENT BASE DATA TXT FILE":str, "LOCATION OF YOUR PATIENT LAB DATA TXT FILE":str)

# calculate patient's age
patient["ID OF THE PATIENT"].age_first_test
```
```
For example, 

```python
patient["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].age_first_test
```
```

will return an integer such as the following output:

```python
>>> 18
```


### To determine whether or not a patient is sick, we use the `is_sick` function stored in the `Patient` Class. should take the data and return a boolean indicating whether the patient has ever had a test with value above (">") or below ("<") the given level. Below is the general instructions of running the function:

```python
from patient_analysis import parse_data

# parse the input files
patient = parse_data('LOCATION OF YOUR PATIENT BASE DATA TXT FILE':str, 'LOCATION OF YOUR PATIENT LAB DATA TXT FILE':str)

# determine whether or not a patient is sick
patient[PATIENT_ID:str].is_sick(LAB_NAME:str, OPERATOR:str, VALUE:float)
```

```

For example, 

```python
patient["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].is_sick("CBC: MCHC", ">", 38.5)
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