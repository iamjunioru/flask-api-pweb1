from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import bcrypt

db = SQLAlchemy()
ma = Marshmallow()

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha_hash = db.Column(db.String(128))  # campo p armazenar a senha em hash
    telefone = db.Column(db.String(15))
    cidade = db.Column(db.String(50))
    pets = db.relationship("Pet", backref="tutor", lazy=True)

    # metodo para definir a senha como um hash
    def set_senha(self, senha):
        self.senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # metodop verificar se uma senha corresponde ao hash armazenado
    def check_senha(self, senha):
        return bcrypt.checkpw(senha.encode('utf-8'), self.senha_hash.encode('utf-8'))
    
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    especie = db.Column(db.String(50))
    tamanho = db.Column(db.String(20)) 
    data_aniversario = db.Column(db.Date) 
    tutor_id = db.Column(db.Integer, db.ForeignKey("tutor.id"), nullable=False)
