from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Salary(db.Model):
    __tablename__ = "salary"
    __table_args__ = (
        db.Index(
            "query_index",
            "employer_name",
            "job_title",
            "employment_start_date",
            "employer_city",
            "employer_state",
        ),
    )
    case_number = db.Column(db.Text, primary_key=True)
    case_status = db.Column(db.Text)
    visa_class = db.Column(db.Text)
    job_title = db.Column(db.Text)
    full_time_position = db.Column(db.Text)
    employment_start_date = db.Column(db.Date)
    employer_name = db.Column(db.Text)
    prevailing_wage = db.Column(db.Float)
    employer_city = db.Column(db.Text)
    employer_state = db.Column(db.Text)
