from datetime import datetime
from flask import Blueprint, render_template, request, redirect, session, flash
from .. import db
from ..models.eqp_manutencao import EquipamentosManutencao, HistEquipamentosManutencao
from ..models.equipamentos import Equipamentos, Status
from ..models.usuarios import Usuarios
from ..services.auth import verify_session_adm
from ..services.graphs import eqp_man, eqp_man_model
from ..services.labels import labels
from ..services.model_manager import ModelManager
from . import key

adm_eqp_man_bp = Blueprint('adm_eqp_man_bp', __name__)


class EquipmentoManutencaoManager(ModelManager):
    def _get_empty_dict(self):
        return {
            'id': '',
            'Serial': '',
            'WI-FI Ip Address': '',
            'Modelo': '',
            'Email do Resp. pela Ocorr.': '',
            'UID do Resp. pela Ocorr.': '',
            'Data de Entrada na Manutenção': '',
            'detail': '...',
        }

    @staticmethod
    def get_equipment_values(equipment):
        return {
            'Serial': equipment.serial,
            'WI-FI Ip Address': equipment.wifi_ip,
            'Modelo': equipment.modelo,
            'Email do Resp. pela Ocorr.': equipment.email_resp_ocorr,
            'UID do Resp. pela Ocorr.': equipment.uid_resp_ocorr,
            'Data de Entrada na Manutenção': equipment.data_entrada.strftime('%d/%m/%Y %H:%M') if isinstance(
                equipment.data_entrada, datetime) else str(equipment.data_entrada),
            'detail': equipment.detail,
        }

    def get_items(self):
        return super().get_items(self.get_equipment_values)

    @staticmethod
    def build_equipment_data(form):
        data = Equipamentos.query.filter_by(serial=form['serial']).first()
        print(data)
        wifi_ip = 'Sem ip'
        modelo = 'Sem modelo'
        if data is not None:
            wifi_ip = data.wifi_ip
            modelo = data.modelo
        unique_fields = {
            'serial': form['serial'],
        }

        field_values = {
            'serial': form['serial'],
            'wifi_ip': wifi_ip,
            'modelo': modelo,
            'email_resp_ocorr': session['email'],
            'uid_resp_ocorr': session['uid'],
            'data_entrada': form['data-de-entrada-na-manutencao'],
            'detail': form['observacao'],
        }

        return unique_fields, field_values


class EquipmentoHistManutencaoManager(ModelManager):
    def _get_empty_dict(self):
        return {
            'id': '',
            'Serial': '',
            'WI-FI Ip Address': '',
            'Modelo': '',
            'Email do Resp. pela Ocorr.': '',
            'UID do Resp. pela Ocorr.': '',
            'Data de Entrada na Manutenção': '',
            'Data de Saida na Manutenção': '',
            'detail': '...',
        }

    @staticmethod
    def get_equipment_values(equipment):
        return {
            'Serial': equipment.serial,
            'Modelo': equipment.modelo,
            'WI-FI Ip Address': equipment.wifi_ip,
            'Email do Resp. pela Ocorr.': equipment.email_resp_ocorr,
            'UID do Resp. pela Ocorr.': equipment.uid_resp_ocorr,
            'Data de Entrada na Manutenção': equipment.data_entrada.strftime('%d/%m/%Y %H:%M') if isinstance(
                equipment.data_entrada, datetime) else str(equipment.data_entrada),
            'Data de Saida na Manutenção': equipment.data_saida.strftime('%d/%m/%Y %H:%M') if isinstance(
                equipment.data_saida, datetime) else str(equipment.data_saida),
            'detail': equipment.detail,
        }

    def get_items(self):
        return super().get_items(self.get_equipment_values)

    @staticmethod
    def build_equipment_data(data):
        unique_fields = {}

        field_values = {
            'serial': data.serial,
            'modelo': data.modelo,
            'wifi_ip': data.wifi_ip,
            'email_resp_ocorr': data.email_resp_ocorr,
            'uid_resp_ocorr': data.uid_resp_ocorr,
            'data_entrada': data.data_entrada,
            'data_saida': datetime.now(),
            'detail': data.detail,
        }

        return unique_fields, field_values


eqp_man_manager = EquipmentoManutencaoManager(EquipamentosManutencao, key, route='eqpManutencao')
eqp_hist_man_manager = EquipmentoHistManutencaoManager(HistEquipamentosManutencao, key, route='eqpManutencao')


@adm_eqp_man_bp.route('/eqpManutencao')
def adm_eqp_manutencao():
    if not verify_session_adm():
        return redirect('/')
    data_eqp_man = eqp_man_manager.get_items()
    data_hist_eqp_man = eqp_hist_man_manager.get_items()
    return render_template('pages/adm_eqp_manutencao.html', data_eqp_man=data_eqp_man,
                           data_hist_eqp_man=data_hist_eqp_man, graph=[eqp_man(), eqp_man_model()], labels=labels())


@adm_eqp_man_bp.route('/editarEqpMan', methods=['POST'])
def editar_eqp_man():
    id_item = request.form['id']
    serial = EquipamentosManutencao.query.filter_by(id=eqp_man_manager.decrypt_id(id_item)).first().serial
    unique_fields, field_values = eqp_man_manager.build_equipment_data(request.form)
    data = Equipamentos.query.filter_by(serial=field_values['serial']).first()
    if data is not None:
        data.status = Status.INDISP
        Equipamentos.query.filter_by(serial=serial).first().status = Status.DISP
        if eqp_man_manager.update_item(id_item, unique_fields, field_values):
            db.session.commit()
            if session['status'] == 'Admin':
                return redirect('/eqpManutencao')
            return redirect('/userEqpManutencao')
    session.pop('_flashes', None)
    flash('O equipamento não está cadastrado.', 'error')
    if session['status'] == 'Admin':
        return redirect('/eqpManutencao')
    return redirect('/userEqpManutencao')


@adm_eqp_man_bp.route('/resgistrarEqpMan', methods=['POST'])
def resgistrar_eqp_man():
    unique_fields, field_values = eqp_man_manager.build_equipment_data(request.form)
    data = Equipamentos.query.filter_by(serial=field_values['serial']).first()
    user = Usuarios.query.filter_by(uid=field_values['uid_resp_ocorr'], email=field_values['email_resp_ocorr']).first()
    if data and user is not None:
        if eqp_man_manager.add_item(unique_fields, field_values):
            data.status = Status.INDISP
            db.session.commit()
        if session['status'] == 'Admin':
            return redirect('/eqpManutencao')
        return redirect('/userEqpManutencao')
    session.pop('_flashes', None)
    session['id_item'] = None
    if user is None:
        flash('O email ou uid do responsavel não existe.', 'error')
    else:
        flash('O equipamento não está cadastrado.', 'error')
    if session['status'] == 'Admin':
        session['route'] = 'eqpManutencao'
        return redirect('/eqpManutencao')
    session['route'] = 'userEqpManutencao'
    return redirect('/userEqpManutencao')



@adm_eqp_man_bp.route('/deletarEqpMan', methods=['POST'])
def deletar_eqp_man():
    id_item = request.get_json().get('id')
    data = EquipamentosManutencao.query.filter_by(id=eqp_man_manager.decrypt_id(id_item)).first()
    unique_fields, field_values = eqp_hist_man_manager.build_equipment_data(data)
    eqp_hist_man_manager.add_item(unique_fields, field_values)
    data = Equipamentos.query.filter_by(serial=data.serial).first()
    data.status = Status.DISP
    if eqp_man_manager.remove_item(id_item):
        return 'O item foi deletado com sucesso!', 200
    return 'Erro ao deletar o item.', 400
