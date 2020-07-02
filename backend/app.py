from flask import Flask, jsonify, request, render_template, session
from flask_graphql import GraphQLView
from schema import schema
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
from models import db, Salary
from helpers import salary_keys, states
from secrets import SECRET_KEY

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../data/salary.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = SECRET_KEY

jwt = JWTManager(app)
db.app = app
db.init_app(app)
swagger = Swagger(app)
api = Api(app)

@swag_from('spect_dict.txt', validation=True)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql", schema=schema, graphiql=True  # for having the GraphiQL interface
    ),
)


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
    params = []
    for d in range(0,4):
        index = str(d+1)
        field = request.args.get("field"+index, None)
        value = request.args.get("value"+index, None)
        if field and value:
            params.append(field.upper())
            params.append(value.upper())
        elif not(field or value):
            params.append("''")
            params.append("")
        else:
            return jsonify({"message": "A parameter is missing."}), 400

    data = db.engine.execute(
        """SELECT * FROM salary WHERE (%s = '%s' AND %s = '%s' AND %s = '%s' AND %s = '%s')
        """
        % (params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7])
    )
    final_result = [dict(i) for i in data]
    return jsonify({"results": final_result}), 200

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
    year = session.get("year")
    year = year[-2:] if year else "%%"  # get year without century
    matched = Salary.query.filter(
        db.or_(Salary.EMPLOYER_NAME.like(fuzzy_query["employer"])),
        db.or_(Salary.JOB_TITLE.like(fuzzy_query["title"])),
        db.or_(Salary.EMPLOYER_CITY.like(fuzzy_query["city"])),
        db.or_(Salary.EMPLOYER_STATE.like(fuzzy_query["state"])),
        db.or_(db.func.substr(Salary.EMPLOYMENT_START_DATE, -2).like(year)),
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
