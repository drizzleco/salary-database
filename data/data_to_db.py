import pandas as pd
import sys
import sqlite3
import os
import wget
from xlsx2csv import Xlsx2csv

name = sys.argv[1]
url = sys.argv[2]

# download data
print("Downloading data for " + name)
xlsx_path = wget.download(url, out="data/{}.xlsx".format(name))

# convert to csv
print()
print("Converting data/{}.xlsx to data/{}.csv".format(name, name))
csv_path = "data/{}.csv".format(name)
Xlsx2csv(xlsx_path, outputencoding="utf-8").convert(csv_path)

# save to db
print("Saving {} to database".format(name))
print("Reading file: " + csv_path)
sheet = pd.read_csv(csv_path)
print("Renaming columns...")
sheet.rename(
    columns={
        "PERIOD_OF_EMPLOYMENT_START_DATE": "EMPLOYMENT_START_DATE",
        "PREVAILING_WAGE_1": "PREVAILING_WAGE",
    },
    inplace=True,
)

PERSON_FIELDS = [
    "CASE_NUMBER",
    "CASE_STATUS",
    "VISA_CLASS",
    "JOB_TITLE",
    "FULL_TIME_POSITION",
    "EMPLOYMENT_START_DATE",
]
EMPLOYER_FIELDS = [
    "EMPLOYER_NAME",
    "PREVAILING_WAGE",
    "EMPLOYER_CITY",
    "EMPLOYER_STATE",
]

# SELECT some important fields
print("Cleaning sheet")
cleaned_sheet = sheet[PERSON_FIELDS + EMPLOYER_FIELDS]
cleaned_sheet = cleaned_sheet[cleaned_sheet["VISA_CLASS"] == "H-1B"]
cleaned_sheet = cleaned_sheet[cleaned_sheet["PREVAILING_WAGE"].notnull()]
cleaned_sheet = cleaned_sheet[cleaned_sheet["CASE_STATUS"] == "CERTIFIED"]
cleaned_sheet = cleaned_sheet[cleaned_sheet["FULL_TIME_POSITION"] == "Y"]


# Make the file if it doesn't exist.
if not os.path.exists("data/salary.sqlite"):
    print("db doesn't exist. creating new db")
    os.mknod("data/salary.sqlite")
print("Connecting to db")
conn = sqlite3.connect("data/salary.sqlite")
print("Saving data to db")
cleaned_sheet.to_sql(name="salary", if_exists="replace", con=conn, index=False)
print("Done!!")
