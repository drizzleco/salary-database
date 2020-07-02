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
        "PERIOD_OF_EMPLOYMENT_START_DATE": "employment_start_date",
        "PREVAILING_WAGE_1": "prevailing_wage",
    },
    inplace=True,
)

PERSON_FIELDS = [
    "case_number",
    "case_status",
    "visa_class",
    "job_title",
    "full_time_position",
    "employment_start_date",
]
EMPLOYER_FIELDS = [
    "employer_name",
    "prevailing_wage",
    "employer_city",
    "employer_state",
]

# SELECT some important fields
print("Cleaning sheet")
cleaned_sheet = sheet[PERSON_FIELDS + EMPLOYER_FIELDS]
cleaned_sheet = cleaned_sheet[cleaned_sheet["visa_class"] == "H-1B"]
cleaned_sheet = cleaned_sheet[cleaned_sheet["prevailing_wage"].notnull()]
cleaned_sheet = cleaned_sheet[cleaned_sheet["case_status"] == "CERTIFIED"]
cleaned_sheet = cleaned_sheet[cleaned_sheet["full_time_position"] == "Y"]


# Make the file if it doesn't exist.
if not os.path.exists("data/salary.sqlite"):
    print("db doesn't exist. creating new db")
    os.mknod("data/salary.sqlite")
print("Connecting to db")
conn = sqlite3.connect("data/salary.sqlite")
print("Saving data to db")
cleaned_sheet.to_sql(name="salary", if_exists="replace", con=conn, index=False)
print("Done!!")
