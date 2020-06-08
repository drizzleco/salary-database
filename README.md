# Salary Database

## Technology
- sqlite3
- python

##  Info
To obtain the H1B data, go to the [site here](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). Then, click on the "Disclosure Data" tab. Once we're here, scroll down to LCA Programs and download the report for the given fiscal year. In my sample, I ran this for 2019. After downloading one of the excel file, open it in your desktop client and export it to csv. Then, use the "Data Ingestion" notebook to clean it up.

Currently, all the information exists in the data folder. I added the steps for moving information in the data ingestion notebook. We can probably automate that to make this idempotent.