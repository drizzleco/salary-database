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

## Feel free to access the GraphQL Viewer!
Using https://salary-database.herokuapp.com/graphql, feel free to take a look at the schema and query the data. Here is an example input
```
{
  salaries(limit: 10, employer: "AIRBNB", year:"2020"){
    caseNumber
    employerName
    jobTitle
    prevailingWage
    employmentStartDate
  }
}   
```
with the following link: [Query Link](https://salary-database.herokuapp.com/graphql?query=%7B%0A%20%20salaries(limit%3A%2010%2C%20employer%3A%20%22AIRBNB%22%2C%20year%3A%20%222020%22)%20%7B%0A%20%20%20%20caseNumber%0A%20%20%20%20employerName%0A%20%20%20%20jobTitle%0A%20%20%20%20prevailingWage%0A%20%20%20%20employmentStartDate%0A%20%20%7D%0A%7D%0A)

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
