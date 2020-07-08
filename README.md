# Salary Database

## Technology

- sqlite3
- python

## Setup

1.  `make install`
2.  `make collect_2019_data` to populate salary db with just 2019 data
3.  add a secrets file

    `backend/secrets.py`

    ```python
    SECRET_KEY = ""
    ```

## Info

To obtain the H1B data, go to the [site here](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). Then, click on the "Disclosure Data" tab. Once we're here, scroll down to LCA Programs and download the report for the given fiscal year. In my sample, I ran this for 2019. After downloading one of the excel file, open it in your desktop client and export it to csv. Then, use the "Data Ingestion" notebook to clean it up.

Currently, all the information exists in the data folder. I added the steps for moving information in the data ingestion notebook. We can probably automate that to make this idempotent.

## Production

**Requirements**

You'll need:

- postgresql
  - install with: `brew install pgloader`
- pgloader
  - install with: `brew install postgresql`
- Heroku CLI

---

In the future, when we want to update the database, the steps to push our local sqlite database to the production heroku database are:

1. use pgloader to load our local sqlite db to a local postgres database
   - `pgloader data/salary.sqlite postgresql:///[name of postgres dev db]`
2. reset remote db
   - `heroku pg:reset DATABASE_URL --app salary-database`
3. push local postgres database to heroku
   - `heroku pg:push postgresql:///[name of postgres dev db] DATABASE_URL --app salary-database`

NOTE: you can use `heroku pg:info --app salary-database` to get info about the the production database and check if we are near the row limit.
