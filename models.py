from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import bcrypt

db = SQLAlchemy()
ma = Marshmallow()

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha_hash = db.Column(db.String(128))
    telefone = db.Column(db.String(15))
    cidade = db.Column(db.String(50))
    pets = db.relationship("Pet", backref="tutor", lazy=True)

    def set_senha(self, senha):
        self.senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_senha(self, senha):
        return bcrypt.checkpw(senha.encode('utf-8'), self.senha_hash.encode('utf-8'))

    def serialize(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "cidade": self.cidade,
            "telefone": self.telefone,
            "pets": [{"id": pet.id, "nome": pet.nome, "especie": pet.especie, "tamanho": pet.tamanho, "tutor_id": pet.tutor_id} for pet in self.pets],
        }

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    especie = db.Column(db.String(50))
    tamanho = db.Column(db.String(20))
    data_aniversario = db.Column(db.Date)
    tutor_id = db.Column(db.Integer, db.ForeignKey("tutor.id"), nullable=False)
