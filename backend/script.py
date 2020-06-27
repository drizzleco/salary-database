import pandas as pd
# It started with a file called H-1B_Disclosure_Data_FY2019.xlsx
# Then, I manually converted it to disclosure_2019.csv using LibreOffice Calc save as CSV
sheet = pd.read_csv("../data/disclosure_2019.csv")

PERSON_FIELDS = ['CASE_NUMBER', 'CASE_STATUS','VISA_CLASS', 'JOB_TITLE', 'FULL_TIME_POSITION', 'PERIOD_OF_EMPLOYMENT_START_DATE']
EMPLOYER_FIELDS = ['EMPLOYER_NAME', 'PREVAILING_WAGE_1', 'EMPLOYER_CITY', 'EMPLOYER_STATE']

# SELECT some important fields
cleaned_sheet = sheet[PERSON_FIELDS + EMPLOYER_FIELDS]
cleaned_sheet = cleaned_sheet[cleaned_sheet['VISA_CLASS'] == 'H-1B']
cleaned_sheet = cleaned_sheet[cleaned_sheet['PREVAILING_WAGE_1'].notnull()]
cleaned_sheet = cleaned_sheet[cleaned_sheet['CASE_STATUS'] == 'CERTIFIED']
cleaned_sheet = cleaned_sheet[cleaned_sheet['FULL_TIME_POSITION'] == 'Y']

import sqlite3
import os
# Make the file if it doesn't exist.
#if not os.path.exists('../data/salary.sqlite'):
    #os.mknod('../data/salary.sqlite')
conn = sqlite3.connect('../data/salary.sqlite')
cleaned_sheet.to_sql(name='salary', if_exists='replace', con=conn, index=False)


tempo = pd.read_sql("SELECT DISTINCT(EMPLOYER_NAME) FROM salary", conn)
boop = [x for x in tempo["EMPLOYER_NAME"].tolist() if x and x[:2] == "AF"]
another_query = pd.read_sql("SELECT * FROM salary WHERE EMPLOYER_NAME = 'AFFIRM, INC.'", conn)
