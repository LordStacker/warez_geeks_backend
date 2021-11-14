from flask import Flask, json, jsonify, request
import re
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from models import Documentation, db, User, Availability
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/warezgeeks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = 'warezone'
app.config["SECRET_KEY"] = "warez-geeks-owners"
app.config['DEBUG'] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db.init_app(app)
Migrate(app, db)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


@app.route("/register", methods=["POST"])
@cross_origin()
def register():
    request.get_json(force=True)
    email = request.json.get("email")
    password = request.json.get("password")
    full_name = request.json.get("full_name")
    last_name = request.json.get("last_name")
    knowledge = request.json.get("knowledge", None)
    phone = request.json.get("phone")
    question = request.json.get("question")
    role = request.json.get("role")
    answer = request.json.get("answer")
    username = request.json.get("username")
    user = User.query.filter_by(email=email, username=username).first()
    if user is None:
        user = User()
        user.full_name = full_name
        user.last_name = last_name
        user.knowledge = knowledge
        user.question = question
        user.phone = phone
        user.answer = answer
        user.username = username
        user.role = role

        # validating email
        email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(email_regex, email):
            user.email = email
        else:
            return jsonify({
                "msg": "email is not valid"
            }), 400

        # validating password
        password_regex = '^.*(?=.{4,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'
        if re.search(password_regex, password):
            password_hash = bcrypt.generate_password_hash(
                password).decode('utf-8')
            user.password = password_hash
        else:
            return jsonify({
                "msg": "password is not valid"
            }), 400
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "msg": "User register succeded"
        }), 200
    else:
        return jsonify({
            "msg": "user already exist"
        }), 400


@app.route("/documentation", methods=["GET", "POST"])
def documents():
    if request.method == "GET":
        documentation = Documentation.query.all()
        documentation = list(map(lambda x: x.serialize(), documentation))
        return jsonify(documentation)
        if documentation is not None:
            return jsonify(documentation)
    else:
        documentation = Documentation()
        documentation.title = request.json.get("title")
        documentation.intro = request.json.get("intro")
        documentation.info = request.json.get("info")
        documentation.info_two = request.json.get("info_two")

        db.session.add(documentation)
        db.session.commit()

    return jsonify(documentation.serialize())


@app.route("/documentation/<int:id>", methods=["GET"])
def Documentsbyid(id):
    documentation = Documentation.query.get(id)
    return jsonify(documentation.serialize())


@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    # request.get_json(force=True)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
   # user = User.query.filter_by(email=email, password=password).first()
    if password is None:
        return jsonify({
            "msg": "Enter a valid password or password is empty"
        }), 400
    if email is None:
        return jsonify({
            "msg": "Enter a valid email or email is empty"
        }), 400

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({
            "msg": "User does not exist, go to register"
        }), 400
    elif bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.email)
        return jsonify({
            "msg": "Logged in succesfully",
            "access_token": access_token,
            "user": user.serialize()
        })
    else:
        return jsonify({
            "msg": "wrong credentials"
        }), 400


@app.route('/me', methods=["POST"])
@jwt_required()
def me():
    user = User()
    current_user = get_jwt_identity()
    current_user_token_expires = get_jwt()["exp"]
    return jsonify({
        "current_user": current_user,
        #"user": user.serialize_just_username(),
        "current_user_token_expires": datetime.
        fromtimestamp(current_user_token_expires)
    }), 200
# @app.route('user/availability', methods=["POST"])
# @jwt_required()
# def add_availability():
    # user id
    # loop en libreria


@app.route('/availability/teacher', methods=["POST"])
def availability():
    availability = Availability()
    start_date = request.json.get("start")
    #start_date = datetime.fromisoformat(start_date)
    #updating
    availability.start = start_date
    end_date = request.json.get("end")
    #end_date = datetime.fromisoformat(end_date)
    availability.end = end_date
    id_user = request.json.get("id_user")
    availability.id_user = id_user    

    db.session.add(availability)
    db.session.commit()
    return jsonify(availability.serialize())

@app.route('/check/availability', methods=["GET"])
def checkAvailability():
    print("Hola")


if __name__ == "__main__":
    app.run(host='localhost', port=8080)
