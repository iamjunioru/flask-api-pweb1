from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from models import db, ma
from resources import TutorResource, PetResource, GetAllResource, authenticate
from config import Config
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
ma.init_app(app)
jwt = JWTManager(app)
api = Api(app)

with app.app_context():
    db.create_all()

@app.route("/")
def welcome():
    return "Welcome to the Tutor and Pet Management API!"

app.add_url_rule("/auth", "authenticate", authenticate, methods=["POST"])

api.add_resource(GetAllResource, "/all")
api.add_resource(TutorResource, "/tutor", "/tutor/<int:tutor_id>")
api.add_resource(PetResource, "/pet", "/pet/<int:pet_id>")

swagger = Swagger(app, template_file="swagger.json")

if __name__ == "__main__":
    app.run(debug=True)
