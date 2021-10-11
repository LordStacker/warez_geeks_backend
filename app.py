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

@app.route("/profile", methods=["POST"])
@cross_origin()
def register():
    request.get_json(force=True)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    full_name = request.json.get("full_name", None)
    last_name= request.json.get("last_name", None)
    
    user = User(email=email, password=password, full_name=full_name, last_name=last_name)
    db.session.add(user)
    db.session.commit()

    return jsonify(user.serialize(),201)
if __name__ == "__main__":
    app.run(host='localhost', port=8080)