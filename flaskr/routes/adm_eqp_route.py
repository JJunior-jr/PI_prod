from flask import Blueprint, render_template, request, redirect
from .adm_eqp_man_route import eqp_man_manager, eqp_hist_man_manager
from flaskr import db
from ..models.eqp_manutencao import EquipamentosManutencao, HistEquipamentosManutencao
from ..models.equipamentos import Equipamentos, Status, Options
from ..services.auth import verify_session_adm
from ..services.graphs import eqp_disp_model_graph
from ..services.labels import labels
from ..services.model_manager import ModelManager
from . import key

adm_eqp_bp = Blueprint('adm_eqp_bp', __name__)

class EquipmentoManager(ModelManager):
    def _get_empty_dict(self):
        return {
            'id': '',
            'Serial': '',
            'WI-FI Ip Address': '',
            'Modelo': '',
            'Status': '',
            'Coldre': '',
            'Alça': '',
            'Touch': '',
            'Som': '',
            'Vibração': '',
            'Gatilho': '',
            'Lazer': ''
        }

    @staticmethod
    def get_equipment_values(equipment):
        return {
            'Serial': equipment.serial,
            'WI-FI Ip Address': equipment.wifi_ip,
            'Modelo': equipment.modelo,
            'Status': equipment.status.value if isinstance(equipment.status, Status) else equipment.status,
            'Coldre': equipment.coldre.value if isinstance(equipment.coldre, Options) else equipment.coldre,
            'Alça': equipment.alca.value if isinstance(equipment.alca, Options) else equipment.alca,
            'Touch': equipment.touch.value if isinstance(equipment.touch, Options) else equipment.touch,
            'Som': equipment.som.value if isinstance(equipment.som, Options) else equipment.som,
            'Vibração': equipment.vibracao.value if isinstance(equipment.vibracao, Options) else equipment.vibracao,
            'Gatilho': equipment.gatilho.value if isinstance(equipment.gatilho, Options) else equipment.gatilho,
            'Lazer': equipment.lazer.value if isinstance(equipment.lazer, Options) else equipment.lazer
        }

    def get_items(self):
        return super().get_items(self.get_equipment_values)

    @staticmethod
    def build_equipment_data(form):
        unique_fields = {
            'serial': form['serial'],
            'wifi_ip': form['wi-fi-ip-address']
        }

        field_values = {
            'serial': form['serial'],
            'wifi_ip': form['wi-fi-ip-address'],
            'modelo': form['modelo'],
            'coldre': Options.SIM if form.get('coldre') == 'Sim' else Options.NAO,
            'alca': Options.SIM if form.get('alca') == 'Sim' else Options.NAO,
            'touch': Options.SIM if form.get('touch') == 'Sim' else Options.NAO,
            'som': Options.SIM if form.get('som') == 'Sim' else Options.NAO,
            'vibracao': Options.SIM if form.get('vibracao') == 'Sim' else Options.NAO,
            'gatilho': Options.SIM if form.get('gatilho') == 'Sim' else Options.NAO,
            'lazer': Options.SIM if form.get('lazer') == 'Sim' else Options.NAO
        }

        return unique_fields, field_values

eqp_manager = EquipmentoManager(Equipamentos, key, route='equipamentosAdm')
@adm_eqp_bp.route('/equipamentosAdm')
def adm_equipamentos():
    if not verify_session_adm():
        return redirect('/')
    data_eqp = eqp_manager.get_items()
    return render_template('pages/adm_equipamentos.html', data_eqp=data_eqp, graph=[eqp_disp_model_graph()], labels=labels())

@adm_eqp_bp.route('/editarEqp', methods=['POST'])
def editar_eqp():
    id_item = request.form['id']
    unique_fields, field_values = eqp_manager.build_equipment_data(request.form)
    serial = Equipamentos.query.filter_by(id=eqp_manager.decrypt_id(id_item)).first().serial

    data = EquipamentosManutencao.query.filter_by(serial=serial).first()
    data_man = HistEquipamentosManutencao.query.filter_by(serial=serial).all()

    if eqp_manager.update_item(id_item, unique_fields, field_values):
        for item in data_man:
                item.wifi_ip = field_values['wifi_ip']
                item.serial = field_values['serial']
                item.modelo = field_values['modelo']
        if data is not None:
            data.wifi_ip = field_values['wifi_ip']
            data.serial = field_values['serial']
            data.modelo = field_values['modelo']
        db.session.commit()
        return redirect('/equipamentosAdm')
    return redirect('/equipamentosAdm')

@adm_eqp_bp.route('/resgistrarEqp', methods=['POST'])
def resgistrar_eqp():
    unique_fields, field_values = eqp_manager.build_equipment_data(request.form)
    if eqp_manager.add_item(unique_fields, field_values):
       return redirect('/equipamentosAdm')
    return redirect('/equipamentosAdm')

@adm_eqp_bp.route('/deletarEqp', methods=['POST'])
def deletar_eqp():
    id_item = request.get_json().get('id')
    data = Equipamentos.query.filter_by(id=eqp_manager.decrypt_id(id_item)).first().serial
    data = EquipamentosManutencao.query.filter_by(serial=data).first()
    if data is not None:
        unique_fields, field_values = eqp_hist_man_manager.build_equipment_data(data)
        eqp_hist_man_manager.add_item(unique_fields, field_values)
        eqp_man_manager.remove_item(eqp_man_manager.encrypt_id(data.id))
    if eqp_manager.remove_item(id_item):
        return 'O item foi deletado com sucesso!', 200
    return 'Erro ao deletar o item.', 400
