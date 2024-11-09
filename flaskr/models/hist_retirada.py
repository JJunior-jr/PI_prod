from flaskr import db
from flaskr.models.equipamentos import Options

class HistEquipamentosRetirados(db.Model):
    __tablename__ = 'hist_equipamentos_retirados'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial = db.Column(db.String(50), nullable=False)
    wifi_ip = db.Column(db.String(120), nullable=False)
    modelo = db.Column(db.String(120), nullable=False)
    responsavel = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    responsavel_retirada = db.Column(db.String(120), nullable=False)
    responsavel_entrega = db.Column(db.String(120), nullable=True)
    uid_responsavel = db.Column(db.String(120), nullable=False)
    data_retirada = db.Column(db.DateTime, nullable=False)
    data_entrega = db.Column(db.DateTime, nullable=True)
    coldre = db.Column(db.Enum(Options), nullable=False)
    alca = db.Column(db.Enum(Options), nullable=False)
    touch = db.Column(db.Enum(Options), nullable=False)
    som = db.Column(db.Enum(Options), nullable=False)
    vibracao = db.Column(db.Enum(Options), nullable=False)
    gatilho = db.Column(db.Enum(Options), nullable=False)
    lazer = db.Column(db.Enum(Options), nullable=False)

    def __repr__(self):
        return (f"('id':'{self.id}','serial':'{self.serial}', 'wifi_ip': '{self.wifi_ip}', "
                f"'modelo': '{self.modelo}','reponsavel': '{self.reponsavel}', 'email': '{self.email}',"
                f"'uid_responsavel': '{self.uid_responsavel}','data_retirada': '{self.data_retirada}','data_entrega': '{self.data_entrega}',"
                f"'coldre': '{self.coldre}', 'alca': '{self.alca}','touch': '{self.touch}',"
                f"'som': '{self.som}', 'vibracao': '{self.vibracao}','gatilho': '{self.gatilho}','lazer': '{self.lazer}')")

class HistEquipamentosRetiradosDivergentes(db.Model):
    __tablename__ = 'hist_equipamentos_retirados_divergentes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial = db.Column(db.String(50), nullable=False)
    wifi_ip = db.Column(db.String(120), nullable=False)
    modelo = db.Column(db.String(120), nullable=False)
    responsavel = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    responsavel_retirada = db.Column(db.String(120), nullable=False)
    responsavel_entrega = db.Column(db.String(120), nullable=True)
    uid_responsavel = db.Column(db.String(120), nullable=False)
    data_retirada = db.Column(db.DateTime, nullable=False)
    data_entrega = db.Column(db.DateTime, nullable=True)
    coldre = db.Column(db.Enum(Options), nullable=False)
    alca = db.Column(db.Enum(Options), nullable=False)
    touch = db.Column(db.Enum(Options), nullable=False)
    som = db.Column(db.Enum(Options), nullable=False)
    vibracao = db.Column(db.Enum(Options), nullable=False)
    gatilho = db.Column(db.Enum(Options), nullable=False)
    lazer = db.Column(db.Enum(Options), nullable=False)

    def __repr__(self):
        return (f"('id':'{self.id}','serial':'{self.serial}', 'wifi_ip': '{self.wifi_ip}', "
                f"'modelo': '{self.modelo}','responsavel': '{self.responsavel}', 'email': '{self.email}',"
                f"'uid_responsavel': '{self.uid_responsavel}','data_retirada': '{self.data_retirada}','data_entrega': '{self.data_entrega}',"
                f"'coldre': '{self.coldre}', 'alca': '{self.alca}','touch': '{self.touch}',"
                f"'som': '{self.som}', 'vibracao': '{self.vibracao}','gatilho': '{self.gatilho}','lazer': '{self.lazer}')")