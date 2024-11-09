from flaskr import db
from enum import Enum


class Status(Enum):
    DISP = "Disponivel"
    INDISP = "Indisponivel"

class Options(Enum):
    SIM = "Sim"
    NAO = "Não"

class Equipamentos(db.Model):
    __tablename__ = 'equipamentos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial = db.Column(db.String(50), unique=True, nullable=False)
    wifi_ip = db.Column(db.String(120), unique=True, nullable=False)
    modelo = db.Column(db.String(120), nullable=False)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.DISP)
    coldre = db.Column(db.Enum(Options), nullable=False)
    alca = db.Column(db.Enum(Options), nullable=False)
    touch = db.Column(db.Enum(Options), nullable=False)
    som = db.Column(db.Enum(Options), nullable=False)
    vibracao = db.Column(db.Enum(Options), nullable=False)
    gatilho = db.Column(db.Enum(Options), nullable=False)
    lazer = db.Column(db.Enum(Options), nullable=False)

    def __repr__(self):
        return (f"('id':'{self.id}','serial':'{self.serial}', 'wifi_ip': '{self.wifi_ip}', "
                f"'modelo': '{self.modelo}','status': '{self.status}', 'coldre': '{self.coldre}',"
                f"'alca': '{self.alca}','touch': '{self.touch}','som': '{self.som}',"
                f"'vibracao': '{self.vibracao}','gatilho': '{self.gatilho}','lazer': '{self.lazer}')")
