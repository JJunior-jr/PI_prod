from flaskr import db

class EquipamentosManutencao(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial = db.Column(db.String(50), unique=True, nullable=False)
    wifi_ip = db.Column(db.String(120), unique=True, nullable=False)
    modelo = db.Column(db.String(120), nullable=False)
    email_resp_ocorr = db.Column(db.String(120), nullable=False)
    uid_resp_ocorr = db.Column(db.String(120), nullable=False)
    data_entrada = db.Column(db.DateTime, nullable=False)
    detail = db.Column(db.String(1024), nullable=False)

    def __repr__(self):
        return (f"('id':'{self.id}','serial':'{self.serial}', 'wifi_ip': '{self.wifi_ip}', "
                f"'modelo': '{self.modelo}','email_resp_ocorr': '{self.email_resp_ocorr}', 'uid_resp_ocorr': '{self.uid_resp_ocorr}', "
                f"'data_entrada': '{self.data_entrada}')")

class HistEquipamentosManutencao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(50), nullable=False)
    wifi_ip = db.Column(db.String(120), nullable=False)
    modelo = db.Column(db.String(120), nullable=False)
    email_resp_ocorr = db.Column(db.String(120), nullable=False)
    uid_resp_ocorr = db.Column(db.String(120), nullable=False)
    data_entrada = db.Column(db.DateTime, nullable=False)
    data_saida = db.Column(db.DateTime, nullable=False)
    detail = db.Column(db.String(1024), nullable=False)

    def __repr__(self):
        return (f"('id':'{self.id}','serial':'{self.serial}', 'wifi_ip': '{self.wifi_ip}', "
                f"'modelo': '{self.modelo}','email_resp_ocorr': '{self.email_resp_ocorr}', 'uid_resp_ocorr': '{self.uid_resp_ocorr}', "
                f"'data_entrada': '{self.data_entrada}', 'data_saida': '{self.data_saida}', 'detail': '{self.detail}')")
