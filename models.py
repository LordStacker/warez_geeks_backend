from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), nullable =False)
    password = db.Column(db.String(10), nullable=False)
    full_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    isActive = db.Column(db.Boolean, default = False)

    def __repr__(self):
        return "<User %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'full_name': self.full_name,
            'last_name': self.last_name       
        }
    def serialize_just_username(self):
        return {
            'id': self.id,
            'email': self.email
        }
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    role = db.Column(db.String(15), nullable = False)
    question = db.Column(db.String(20), nullable = False)
    answer = db.Column(db.String(20), nullable = False)
    knowledge = db.Column(db.String(20), nullable = False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    rating = db.relationship('Rating', backref='profile', lazy=True)
    request = db.relationship('Request', backref='profile', lazy=True)

    def __repr__(self):
        return "<Profile %r>" % self.id
        
    def serialize(self):
        return {
            'id': self.id,
            'role': self.role,
            'question': self.question,
            'answer': self.answer,
            'knowledge': self.knowledge      
        }
    def serialize_just_Profile(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer
        }
class Request(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    request_status = db.Column(db.String(50), nullable = False)
    date = db.Column(db.String(50), nullable = False)
    hour = db.Column(db.String(10), nullable = False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    id_profile = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable = False)

    def __repr__(self):
        return "<Request %r>" % self.id
        
    def serialize(self):
        return {
            'id': self.id,
            'request_status': self.request_status,
            'date': self.date,
            'hour': self.hour     
        }
    def serialize_just_Request(self):
        return {
            'id': self.id,
            'request_status': self.request_status,
            'date': self.date,
            'hour': self.hour
        }
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_profile = db.Column(db.String(20), nullable = False)
    rating = db.Column(db.String(20), nullable = False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable = False)

    def __repr__(self):
        return "<Rating %r>" % self.id
        
    def serialize(self):
        return {
            'id': self.id,
            'id_profile': self.id_profile,
            'rating': self.rating,
            'profile_id': self.profile_id     
        }
    def serialize_just_Profile(self):
        return {
            'id_profile': self.id_profile
        }
class Service(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name_service = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return "<Service %r>" % self.id
        
    def serialize(self):
        return {
            'id': self.id,
            'name_service': self.name_service   
        }
    def serialize_just_Service(self):
        return {
            'id': self.id,
            'name_service': self.name_service
        }
class Availability(db.Model):
    id = db.Column(db.Integer, primary_key = True )
    date = db.Column(db.String(20), nullable = False)
    hour = db.Column(db.String(20), nullable = False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return "<Availability %r>" % self.id
        
    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'hour': self.hour,
            'id_user': self.id_user   
        }
    def serialize_just_Availability(self):
        return {
            'id': self.id,
            'date': self.date,
            'hour': self.hour
        }