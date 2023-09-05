from flask_restful import Resource, reqparse
from flask import jsonify, request
from models import db, Tutor, Pet
from datetime import datetime
from flask_jwt_extended import jwt_required, create_access_token

def authenticate():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    user = Tutor.query.filter_by(email=email).first()
    if user and user.check_senha(senha):
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200
    else:
        return {"message": "Email or password is invalid"}, 401
class GetAllResource(Resource):
    @jwt_required()
    def get(self):
        tutors = Tutor.query.all()
        tutors_data = [t.serialize() for t in tutors]
        return tutors_data, 200
class TutorResource(Resource):
    def format_tutor_data(self, tutor):
        return {
            "id": tutor.id,
            "nome": tutor.nome,
            "email": tutor.email,
            "senha": tutor.senha_hash,
            "cidade": tutor.cidade,
            "telefone": tutor.telefone,
            "pets": [{"id": pet.id, "nome": pet.nome, "especie": pet.especie, "tamanho": pet.tamanho, "tutor_id": pet.tutor_id} for pet in tutor.pets],
        }
        
    @jwt_required()
    def get(self, tutor_id=None):
        if tutor_id is None:
            return jsonify({"message": "Put the tutor's ID"}), 400

        tutor = Tutor.query.get(tutor_id)
        if not tutor:
            return jsonify({"message": "Tutor not found"})

        tutor_data = tutor.serialize()
        return tutor_data, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("nome", type=str, required=True)
        parser.add_argument("email", type=str, required=True)
        parser.add_argument("senha", type=str, required=True)
        parser.add_argument("telefone", type=str, required=True)
        parser.add_argument("cidade", type=str, required=True)
        args = parser.parse_args()

        novo_tutor = Tutor(nome=args["nome"], email=args["email"], telefone=args["telefone"], cidade=args["cidade"])
        novo_tutor.set_senha(args["senha"])

        db.session.add(novo_tutor)
        db.session.commit()

        tutor_data = novo_tutor.serialize()
        return tutor_data, 200
        # return jsonify({"message": "Tutor created successfully", "tutor": self.format_tutor_data(novo_tutor)}), 201       
    
    @jwt_required()
    def put(self, tutor_id):
        tutor = Tutor.query.get(tutor_id)
        if not tutor:
            return jsonify({"message": "Tutor not found"})

        parser = reqparse.RequestParser()
        parser.add_argument("nome", type=str, required=True)
        parser.add_argument("email", type=str, required=True)
        parser.add_argument("senha", type=str, required=True)
        parser.add_argument("telefone", type=str, required=True)
        parser.add_argument("cidade", type=str, required=True)
        args = parser.parse_args()

        tutor.nome = args["nome"]
        tutor.email = args["email"]
        tutor.senha = args["senha"]
        tutor.telefone = args["telefone"]
        tutor.cidade = args["cidade"]
        db.session.commit()

        return ({"message": "Tutor updated successfully"}), 200
        # return jsonify({"message": "Tutor updated successfully", "tutor": self.format_tutor_data(tutor)})
    @jwt_required()
    def delete(self, tutor_id):
        tutor = Tutor.query.get(tutor_id)
        if not tutor:
            return jsonify({"message": "Tutor not found"})

        if tutor.pets:
            return jsonify({"message": "Tutor has associated pets and cannot be deleted"})

        db.session.delete(tutor)
        db.session.commit()

        return ({"message": "Tutor deleted successfully"}), 200
        return jsonify({"message": "Tutor deleted successfully"})


class PetResource(Resource):
    @jwt_required()
    def get(self, pet_id=None, tutor_id=None):
        if pet_id is not None:
            pet = Pet.query.get(pet_id)
            if not pet:
                return {"message": "Pet not found"}, 404
            pet_data = {"id": pet.id, "nome": pet.nome,  "especie": pet.especie, "tamanho": pet.tamanho, "tutor_id": pet.tutor_id}
            return pet_data

        if tutor_id is not None:
            pets = Pet.query.filter_by(tutor_id=tutor_id).all()
            pets_data = [{"id": pet.id, "nome": pet.nome, "especie": pet.especie, "tamanho": pet.tamanho, "tutor_id": pet.tutor_id} for pet in pets]
            return jsonify(pets_data)
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("nome", type=str, required=True)
        parser.add_argument("especie", type=str, required=True)
        parser.add_argument("tamanho", type=str, required=True) 
        parser.add_argument("data_aniversario", type=str, required=True) 
        parser.add_argument("tutor_id", type=int, required=True)
        args = parser.parse_args()

        tutor = Tutor.query.get(args["tutor_id"])
        if not tutor:
            return {"message": "Tutor not found"}, 404

        data_aniversario = datetime.strptime(args["data_aniversario"], "%d-%m-%Y").date()

        pet = Pet(nome=args["nome"], especie=args["especie"], tamanho=args["tamanho"], data_aniversario=data_aniversario, tutor=tutor)
        db.session.add(pet)
        db.session.commit()

        pet_data = {
            "id": pet.id,
            "nome": pet.nome,
            "especie": pet.especie,
            "tamanho": pet.tamanho,
            "data_aniversario": args["data_aniversario"], 
            "tutor_id": pet.tutor_id
        }

        return pet_data, 200
    @jwt_required()
    def put(self, pet_id):
        pet = Pet.query.get(pet_id)
        if not pet:
            return jsonify({"message": "Pet not found"})

        parser = reqparse.RequestParser()
        parser.add_argument("nome", type=str, required=True)
        parser.add_argument("especie", type=str, required=True)
        parser.add_argument("tamanho", type=str, required=True)
        parser.add_argument("data_aniversario", type=str, required=True)
        args = parser.parse_args()
        
        data_aniversario = datetime.strptime(args["data_aniversario"], "%d-%m-%Y").date()

        pet.nome = args["nome"]
        pet.especie = args["especie"]
        pet.tamanho = args["tamanho"]
        pet.data_aniversario = data_aniversario
        db.session.commit()

        return ({"message": "Pet updated successfully"}), 200
    
    @jwt_required()
    def delete(self, pet_id):
        pet = Pet.query.get(pet_id)
        if not pet:
            return jsonify({"message": "Pet not found"})

        db.session.delete(pet)
        db.session.commit()
        return jsonify({"message": "Pet deleted successfully"})
