from flask import Flask, jsonify, request, render_template, session
from flask_graphql import GraphQLView
from backend.schema import schema
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    get_raw_jwt,
    jwt_required,
)
from sqlalchemy import text
from flasgger import Swagger, swag_from, SwaggerView, Schema, fields
from flask_restful import Api, Resource
from backend.models import db, Salary
from backend.helpers import SALARY_KEYS, QUERY_KEYS, STATES
import random

app = Flask(__name__)
CORS(app)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgres://mtscouwjvpgsvj:d1df6ddc0071c78af5befa14e2fdf89b8faf6bfe58074d03c9345eed337b3cc9@ec2-52-202-66-191.compute-1.amazonaws.com:5432/d7fqshecacpm5u"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "".join([chr(random.randint(65, 92)) for _ in range(50)])

jwt = JWTManager(app)
db.app = app
db.init_app(app)
swagger = Swagger(app)
api = Api(app)


@swag_from("spect_dict.txt", validation=True)
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
    """
    Home page route
    """
    form_values = {}
    for query in QUERY_KEYS:
        value = request.args.get(query, session.get(query, "")).strip()
        form_values[query] = value
        session[query] = value
    ppl = [
        {key: salary.__dict__[key] for key in SALARY_KEYS}
        for salary in Salary.query.limit(10).all()
    ]
    return render_template("index.html", states=STATES, form_values=form_values)


@app.route("/data/", methods=["GET"])
def employer():
    params = []
    for d in range(0, 4):
        index = str(d + 1)
        field = request.args.get("field" + index, None)
        value = request.args.get("value" + index, None)
        if field and value:
            params.append(field.upper())
            params.append(value.upper())
        elif not (field or value):
            params.append("''")
            params.append("")
        else:
            return jsonify({"message": "A parameter is missing."}), 400

    data = db.engine.execute(
        """SELECT * FROM salary WHERE (%s = '%s' AND %s = '%s' AND %s = '%s' AND %s = '%s')
        """
        % (
            params[0],
            params[1],
            params[2],
            params[3],
            params[4],
            params[5],
            params[6],
            params[7],
        )
    )
    final_result = [dict(i) for i in data]
    return jsonify({"results": final_result}), 200

    db.session.commit()
    return jsonify(message="success"), 200


# GraphQL page route
app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
)


@app.route("/table", methods=["GET"])
def table():
    """
    Endpoint used by table in frontend to fetch salary data 

    Retrieves filter queries from Session and returns sorted and 
    paginated data according to the limit, offset, sort, and order
    query params

    Query string:
        - limit(str) - max number of results to return
        - offset(str) - starting point of data
        - sort(str) - column to sort data by. default: prevailing_wage
        - order(str) - how to order column being sorted(asc or desc). default: asc
    returns:
        matched salary data in form of dict with keys:
            - total - total number of matched results. not the same as limit
            - rows - matched salary data in current page as a list
    """
    max_results = int(request.args.get("limit"))
    offset = int(request.args.get("offset"))
    page = offset // max_results
    sort_by = request.args.get("sort", "prevailing_wage")
    order = request.args.get("order", "asc")
    fuzzy_query = {}
    for query in QUERY_KEYS:
        fuzzy_query[query] = "%{}%".format(session[query])
    matched = Salary.query.filter(
        db.or_(Salary.employer_name.like(fuzzy_query["employer"])),
        db.or_(Salary.job_title.like(fuzzy_query["title"])),
        db.or_(Salary.employer_city.like(fuzzy_query["city"])),
        db.or_(Salary.employer_state.like(fuzzy_query["state"])),
        db.or_(
            db.cast(db.extract("year", Salary.employment_start_date), db.String).like(
                fuzzy_query["year"]
            )
        ),
    )

    rows = [
        {key: salary.__dict__[key] for key in SALARY_KEYS}
        for salary in matched.order_by(getattr(getattr(Salary, sort_by), order)())
        .paginate(page + 1, max_results, False)
        .items
    ]
    return jsonify({"total": matched.count(), "rows": rows})


@app.route("/about", methods=["GET"])
def about():
    """
    About page route
    """
    return render_template("about.html")


@app.route("/api", methods=["GET"])
def api_ref():
    """
    API Reference page route
    """
    return render_template("api.html")


if __name__ == "__main__":
    app.run(debug=True)
