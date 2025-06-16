from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='paciente')  # Novo campo para definir o papel do usuário (default 'paciente')
    is_active = db.Column(db.Boolean, default=True)  # Adicionando o campo is_active

    def __repr__(self):
        return f'<User {self.email}>'


class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="pendente")  # Status: pendente ou aceito
    paciente_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    paciente = db.relationship('User', foreign_keys=[paciente_id], backref='consultas_paciente')
    medico = db.relationship('User', foreign_keys=[medico_id], backref='consultas_medico')

    def __repr__(self):
        return f'<Consulta {self.id} - {self.data_hora}>'