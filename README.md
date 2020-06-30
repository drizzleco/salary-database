# Salary Database

## Technology

- sqlite3
- python

## Setup

1.  `make install`
2.  `make collect_data` to populate salary db

    To download data individually, run:

    `python data/data_to_db.py [NAME OF FILE TO SAVE AS] [DOWNLOAD URL]`

    EX, to just download 2019 disclosure data:

    `python data/data_to_db.py disclosure_2019 https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2019/H-1B_Disclosure_Data_FY2019.xlsx`

3.  add a secrets file

    `backend/secrets.py`

    ```python
    SECRET_KEY = ""
    ```

## Info

To obtain the H1B data, go to the [site here](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). Then, click on the "Disclosure Data" tab. Once we're here, scroll down to LCA Programs and download the report for the given fiscal year. In my sample, I ran this for 2019. After downloading one of the excel file, open it in your desktop client and export it to csv. Then, use the "Data Ingestion" notebook to clean it up.

Currently, all the information exists in the data folder. I added the steps for moving information in the data ingestion notebook. We can probably automate that to make this idempotent.
