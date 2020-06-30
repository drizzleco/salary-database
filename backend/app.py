import csv, sqlite3
import pandas as pd
import jwt as jwt_decode
from flask import Flask, jsonify, request
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

from script import cleaned_sheet

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../data/salary.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)
db.app = app
db.init_app(app)

@app.route("/data/", methods=['GET'])
def employer():

    field = request.args.get("field", None).upper()
    value = request.args.get("value", None).upper()
    
    if not field:
        return jsonify({"message": "Field is required."}), 400
    if not value:
        return jsonify({"message": "Value is required."}), 400

    data = db.engine.execute("""SELECT * FROM salary WHERE %s = '%s'
        """ % (field, value, ))
    
    final_result = [dict(i) for i in data]
    return jsonify({"results": final_result}), 400
    db.session.commit()
    return jsonify(message="success"), 200
    

if __name__ == "__main__":
    app.run(debug=True)

