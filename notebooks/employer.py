import csv, sqlite3
import pandas as pd

sheet = pd.read_csv("../data/disclosure_2019.csv")
table_name = 'employer_info'
file_name = '../data/disclosure_2019.csv'

EMPLOYER_FIELDS = ['EMPLOYER_NAME', 'PREVAILING_WAGE_1', 'EMPLOYER_CITY', 'EMPLOYER_STATE']
employer_sheet = sheet[EMPLOYER_FIELDS]

conn = sqlite3.connect('../data/employers.sqlite')
employer_sheet.to_sql(table_name, conn, if_exists='append', index=False)

test = pd.read_sql("SELECT DISTINCT(EMPLOYER_NAME) FROM employer_info", conn)

conn.commit()
