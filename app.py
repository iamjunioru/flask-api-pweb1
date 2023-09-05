from flask import Flask, request
from flask_restful import Api
from models import db, ma
from resources import TutorResource, PetResource, GetAllResource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import Tutor

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

api = Api(app)
db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def welcome():
    return "Welcome to the Tutor and Pet Management API!"

@app.route("/auth", methods=["POST"])
def authenticate():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    user = Tutor.query.filter_by(email=email).first()
    if user and user.check_senha(senha):
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200
    else:
        return {"message": "email or pass invalid"}, 401

api.add_resource(GetAllResource, "/all") 
api.add_resource(TutorResource, "/tutor", "/tutor/<int:tutor_id>")
api.add_resource(PetResource, "/pet", "/pet/<int:pet_id>")

if __name__ == "__main__":
    app.run(debug=True)
