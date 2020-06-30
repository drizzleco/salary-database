from flask import Flask, render_template, jsonify, session, request
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/salary.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Salary(db.Model):
    CASE_NUMBER = db.Column(db.Text, primary_key=True)
    CASE_STATUS = db.Column(db.Text)
    VISA_CLASS = db.Column(db.Text)
    JOB_TITLE = db.Column(db.Text)
    FULL_TIME_POSITION = db.Column(db.Text)
    PERIOD_OF_EMPLOYMENT_START_DATE = db.Column(db.Text)
    EMPLOYER_NAME = db.Column(db.Text)
    PREVAILING_WAGE_1 = db.Column(db.Integer)
    EMPLOYER_CITY = db.Column(db.Text)
    EMPLOYER_STATE = db.Column(db.Text)

    # @hybrid_property
    # def year(self):
    #     for format in ["%m-%d-%y", "%m/%d/%Y"]:
    #         try:
    #             return datetime.strptime(
    #                 Salary.query.filter(Salary.CASE_NUMBER == self.CASE_NUMBER)
    #                 .first()
    #                 .PERIOD_OF_EMPLOYMENT_START_DATE,
    #                 format,
    #             ).year
    #         except ValueError:
    #             pass
    #     raise ValueError("not a valid date format")


keys = [
    "CASE_NUMBER",
    "CASE_STATUS",
    "VISA_CLASS",
    "JOB_TITLE",
    "FULL_TIME_POSITION",
    "PERIOD_OF_EMPLOYMENT_START_DATE",
    "EMPLOYER_NAME",
    "PREVAILING_WAGE_1",
    "EMPLOYER_CITY",
    "EMPLOYER_STATE",
]

states = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}


@app.route("/", methods=["GET"])
def home():
    form_values = {}
    for query in ["employer", "title", "city", "state", "year"]:
        value = request.args.get(query, session.get(query, "")).strip()
        form_values[query] = value
        session[query] = value
    ppl = [
        {key: salary.__dict__[key] for key in keys}
        for salary in Salary.query.limit(10).all()
    ]
    return render_template("index.html", states=states, form_values=form_values)


@app.route("/data", methods=["GET"])
def data():
    max_results = int(request.args.get("limit"))
    offset = int(request.args.get("offset"))
    page = offset // max_results
    fuzzy_query = {}
    for query in ["employer", "title", "city", "state"]:
        fuzzy_query[query] = "%{}%".format(session[query])
    matched = Salary.query.filter(
        db.or_(Salary.EMPLOYER_NAME.like(fuzzy_query["employer"])),
        db.or_(Salary.JOB_TITLE.like(fuzzy_query["title"])),
        db.or_(Salary.EMPLOYER_CITY.like(fuzzy_query["city"])),
        db.or_(Salary.EMPLOYER_STATE.like(fuzzy_query["state"])),
        # db.or_(Salary.year == int(session.get("year"))),  # this doesn't work
    )

    rows = [
        {key: salary.__dict__[key] for key in keys}
        for salary in matched.paginate(page + 1, max_results, False).items
    ]
    return jsonify({"total": matched.count(), "rows": rows})


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/api", methods=["GET"])
def api():
    return render_template("api.html")


app.run(debug=True)
