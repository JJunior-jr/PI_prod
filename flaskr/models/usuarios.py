from werkzeug.security import generate_password_hash, check_password_hash
from flaskr import db
from enum import Enum

class Status(Enum):
    ADM = "Admin"
    USER = "Usuário"

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    uid = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.USER)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"('id':'{self.id}','name':'{self.name}', 'email': '{self.email}', 'uid': '{self.uid}','status': '{self.status}')"