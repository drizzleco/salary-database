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

from script import cleaned_sheet

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///salary.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)
db.app = app
db.init_app(app)
    

@app.route("/employer/", methods=['GET'])
def employer():
    try:      
        conn = sqlite3.connect('../data/salary.sqlite')
    except sqlite3.Error:
        return jsonify({"message": "Unable to connect to the database."}), 400

    field = request.args.get("field", None)
    value = request.args.get("value", None)
    
    if not field:
        return jsonify({"message": "Field is required."}), 400
    if not value:
        return jsonify({"message": "Value is required."}), 400

    data = pd.read_sql("SELECT * FROM salary WHERE EMPLOYER_NAME = 'AARP'", conn)
    results = data.values.tolist()
    return jsonify({"results": results}), 400
    db.session.commit()
    return jsonify(message="success"), 200
    

if __name__ == "__main__":
    app.run(debug=True)

