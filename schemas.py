from marshmallow import Schema, fields, validate

class TutorSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    email = fields.Email(required=True)
    senha = fields.Str(required=True, validate=validate.Length(min=6))
    telefone = fields.Str(required=True)
    cidade = fields.Str(required=True)

class PetSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    especie = fields.Str(required=True)
    tamanho = fields.Str(required=True)
    data_aniversario = fields.Date(format='%d-%m-%Y', required=True)
    tutor_id = fields.Int(required=True)
