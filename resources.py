from flask_restful import Resource, reqparse
from flask import jsonify
from models import db, Tutor, Pet
from datetime import datetime


class GetAllResource(Resource):
    def get(self):
        tutors = Tutor.query.all()
        tutors_data = []

        for tutor in tutors:
            tutor_data = {
                "id": tutor.id,
                "nome": tutor.nome,
                "email": tutor.email,
                "senha_hash": tutor.senha_hash,
                "cidade": tutor.cidade,
                "telefone": tutor.telefone,
                "pets": [{"id": pet.id, "nome": pet.nome, "especie": pet.especie} for pet in tutor.pets],
            }
            # tutors_data.append(tutor_data)
            tutors_data.append({
                "id": tutor_data["id"],
                "nome": tutor_data["nome"],
                "email": tutor_data["email"],
                "senha_hash": tutor_data["senha_hash"],
                "cidade": tutor_data["cidade"],
                "telefone": tutor_data["telefone"],
                "pets": tutor_data["pets"],
             })

        return jsonify(tutors_data)

class TutorResource(Resource):
    def format_tutor_data(self, tutor):
        return {
            "id": tutor.id,
            "nome": tutor.nome,
            "email": tutor.email,
            "senha_hash": tutor.senha_hash,
            "cidade": tutor.cidade,
            "telefone": tutor.telefone,
            "pets": [{"id": pet.id, "nome": pet.nome} for pet in tutor.pets],
        }

    def get(self, tutor_id=None):
        if tutor_id is None:
            return jsonify({"message": "Coloque o ID do tutor"}), 400

        tutor = Tutor.query.get(tutor_id)
        if not tutor:
            return jsonify({"message": "Tutor not found"})
        
        tutor_data = self.format_tutor_data(tutor)
        return jsonify(tutor_data)

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

        tutor_data = self.format_tutor_data(novo_tutor)
        # return tutor_data, 200
        return jsonify({"tutor": tutor_data})

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

        return jsonify({"message": "Tutor updated successfully", "tutor": self.format_tutor_data(tutor)})

    def delete(self, tutor_id):
        tutor = Tutor.query.get(tutor_id)
        if not tutor:
            return jsonify({"message": "Tutor not found"})

        if tutor.pets:
            return jsonify({"message": "Tutor has associated pets and cannot be deleted"})

        db.session.delete(tutor)
        db.session.commit()

        return jsonify({"message": "Tutor deleted successfully"})


class PetResource(Resource):
    def get(self, pet_id=None, tutor_id=None):
        if pet_id is not None:
            pet = Pet.query.get(pet_id)
            if not pet:
                return {"message": "Pet not found"}, 404
            pet_data = {"id": pet.id, "nome": pet.nome, "tutor_id": pet.tutor_id}
            return jsonify(pet_data)

        if tutor_id is not None:
            pets = Pet.query.filter_by(tutor_id=tutor_id).all()
            pets_data = [{"id": pet.id, "nome": pet.nome, "tutor_id": pet.tutor_id} for pet in pets]
            return jsonify(pets_data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("nome", type=str, required=True)
        parser.add_argument("especie", type=str, required=True)
        parser.add_argument("tamanho", type=str, required=True) 
        parser.add_argument("data_aniversario", type=str, required=True) 
        parser.add_argument("tutor_id", type=int, required=True)
        args = parser.parse_args()

        # errors = pet_schema.validate(args)
        # if errors:
        #    return jsonify({"errors": errors}), 400

        tutor = Tutor.query.get(args["tutor_id"])
        if not tutor:
            return jsonify({"message": "Tutor not found"})
        

        # ("01-12-2023")
        data_aniversario = datetime.strptime(args["data_aniversario"], "%d-%m-%Y").date()

        pet = Pet(nome=args["nome"], especie=args["especie"], tamanho=args["tamanho"], data_aniversario=data_aniversario, tutor=tutor)
        db.session.add(pet)
        db.session.commit()
        pet_data = {"id": pet.id, "nome": pet.nome, "especie": pet.especie, "tamanho": pet.tamanho, "data_aniversario": pet.data_aniversario, "tutor_id": pet.tutor_id}
        return jsonify({"message": "Pet created successfully", "pet": pet_data})

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

        return jsonify({"message": "Pet updated successfully", "pet": {"id": pet.id, "nome": pet.nome, "especie": pet.especie, "tamanho": pet.tamanho, "data_aniversario": pet.data_aniversario, "tutor_id": pet.tutor_id}})

    def delete(self, pet_id):
        pet = Pet.query.get(pet_id)
        if not pet:
            return jsonify({"message": "Pet not found"})

        db.session.delete(pet)
        db.session.commit()
        return jsonify({"message": "Pet deleted successfully"})
