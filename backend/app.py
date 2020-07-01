from flask import Flask, jsonify, request, render_template, session
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    get_raw_jwt,
    jwt_required,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from helpers import salary_keys, states
from secrets import SECRET_KEY

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../data/salary.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = SECRET_KEY

db = SQLAlchemy(app)
jwt = JWTManager(app)
db.app = app
db.init_app(app)


class Salary(db.Model):
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


@app.route("/", methods=["GET"])
def home():
    form_values = {}
    for query in ["employer", "title", "city", "state", "year"]:
        value = request.args.get(query, session.get(query, "")).strip()
        form_values[query] = value
        session[query] = value
    ppl = [
        {key: salary.__dict__[key] for key in salary_keys}
        for salary in Salary.query.limit(10).all()
    ]
    return render_template("index.html", states=states, form_values=form_values)


@app.route("/data/", methods=["GET"])
def employer():

    field = request.args.get("field", None).upper()
    value = request.args.get("value", None).upper()

    if not field:
        return jsonify({"message": "Field is required."}), 400
    if not value:
        return jsonify({"message": "Value is required."}), 400

    data = db.engine.execute(
        """SELECT * FROM salary WHERE %s = '%s'
        """
        % (field, value,)
    )

    final_result = [dict(i) for i in data]
    return jsonify({"results": final_result}), 400
    db.session.commit()
    return jsonify(message="success"), 200


@app.route("/table", methods=["GET"])
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
        {key: salary.__dict__[key] for key in salary_keys}
        for salary in matched.paginate(page + 1, max_results, False).items
    ]
    return jsonify({"total": matched.count(), "rows": rows})


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/api", methods=["GET"])
def api():
    return render_template("api.html")


if __name__ == "__main__":
    app.run(debug=True)

