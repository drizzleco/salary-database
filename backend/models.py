from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Salary(db.Model):
    __tablename__ = "salary"
    CASE_NUMBER = db.Column(db.Text, primary_key=True)
    CASE_STATUS = db.Column(db.Text)
    VISA_CLASS = db.Column(db.Text)
    JOB_TITLE = db.Column(db.Text)
    FULL_TIME_POSITION = db.Column(db.Text)
    EMPLOYMENT_START_DATE = db.Column(db.Text)
    EMPLOYER_NAME = db.Column(db.Text)
    PREVAILING_WAGE = db.Column(db.Integer)
    EMPLOYER_CITY = db.Column(db.Text)
    EMPLOYER_STATE = db.Column(db.Text)
