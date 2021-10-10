from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from models import db, User
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/warezgeeks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db.init_app(app)
Migrate(app, db)


@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    request.get_json(force=True)
    print(request.json)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    # create a new token with the user id inside
    return jsonify({ "msg": "Logged in succesfully" })
@app.route("/Profile", methods=["PUT"])
@cross_origin()
def Profile(): 
    user = Profile
    body = request.get_json(force=False)
    role = body.get("role", None)
    email = body.get("email", None)
    user.role = role
    user.email = email

    db.session.commit()
    return ("done")

if __name__ == '__main__':
    app.run(host='localhost', port=8080)