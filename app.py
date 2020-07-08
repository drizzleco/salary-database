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
import random

app = Flask(__name__)
CORS(app)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgres://mtscouwjvpgsvj:d1df6ddc0071c78af5befa14e2fdf89b8faf6bfe58074d03c9345eed337b3cc9@ec2-52-202-66-191.compute-1.amazonaws.com:5432/d7fqshecacpm5u"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "".join([chr(random.randint(65, 92)) for _ in range(50)])

db = SQLAlchemy(app)
jwt = JWTManager(app)
db.app = app
db.init_app(app)


class Salary(db.Model):
    case_number = db.Column(db.Text, primary_key=True)
    case_status = db.Column(db.Text)
    visa_class = db.Column(db.Text)
    job_title = db.Column(db.Text)
    full_time_position = db.Column(db.Text)
    employment_start_date = db.Column(db.Text)
    employer_name = db.Column(db.Text)
    prevailing_wage = db.Column(db.Integer)
    employer_city = db.Column(db.Text)
    employer_state = db.Column(db.Text)


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
        db.or_(Salary.employer_name.like(fuzzy_query["employer"])),
        db.or_(Salary.job_title.like(fuzzy_query["title"])),
        db.or_(Salary.employer_city.like(fuzzy_query["city"])),
        db.or_(Salary.employer_state.like(fuzzy_query["state"])),
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

