from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from models import Profile, db, User
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
    #request.get_json(force=True)
    print(request.json)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

   # user = User.query.filter_by(email=email, password=password).first()
    username = User.query.filter_by(email=email).first()
    if username is None:
        return jsonify({"msg": "email invalid or misspelled"}), 401
    else:
        user = User.query.filter_by(email=email, password=password).first()
        if user is None:

            return jsonify({"msg": "Bad password"}), 401

    return jsonify({"msg": "Logged in succesfully"})


@app.route("/profile", methods=["POST"])
@cross_origin()
def register():
    request.get_json(force=True)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    full_name = request.json.get("full_name", None)
    last_name = request.json.get("last_name", None)
    knowledge = request.json.get("knowledge", None)
    phone = request.json.get("phone", None)
    question = request.json.get("question", None)
    answer = request.json.get("answer", None)
    username = request.json.get("username", None)

    user = User(email=email,
                password=password,
                full_name=full_name,
                last_name=last_name,
                knowledge=knowledge,
                phone=phone,
                question=question,
                answer=answer,
                username=username)

    db.session.add(user)
    db.session.commit()

    return jsonify(user.serialize(), 201)


if __name__ == "__main__":
    app.run(host='localhost', port=8080)
