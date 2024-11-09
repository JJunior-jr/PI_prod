from datetime import datetime
from flask import Blueprint, render_template, redirect, request
from .. import db
from ..models.equipamentos import Options
from ..models.hist_retirada import HistEquipamentosRetirados, HistEquipamentosRetiradosDivergentes
from ..services.auth import verify_session
from . import key
from ..services.graphs import eqp_ret, eqp_disp_model_graph
from ..services.labels import labels
from ..services.model_manager import ModelManager

adm_hist_ret_bp = Blueprint('adm_hist_ret_bp', __name__)


class HistRetiradaManager(ModelManager):
    def _get_empty_dict(self):
        return {
            'id': '',
            'Serial': '',
            'WI-FI Ip Address': '',
            'Modelo': '',
            'Coldre': '',
            'Alça': '',
            'Touch': '',
            'Som': '',
            'Vibração': '',
            'Gatilho': '',
            'Lazer': '',
            'Responsável': '',
            'Email do Responvável': '',
            'UID do Responsável.': '',
            'Email do Resp. pela Retirada.': '',
            'Email do Resp. pela Entrega.': '',
            'Data de Retirada': '',
            'Data de Entega': '',
        }

    @staticmethod
    def get_equipment_values(equipment):
        return {
            'Serial': equipment.serial,
            'WI-FI Ip Address': equipment.wifi_ip,
            'Modelo': equipment.modelo,
            'Coldre': equipment.coldre.value if isinstance(equipment.coldre, Options) else equipment.coldre,
            'Alça': equipment.alca.value if isinstance(equipment.alca, Options) else equipment.alca,
            'Touch': equipment.touch.value if isinstance(equipment.touch, Options) else equipment.touch,
            'Som': equipment.som.value if isinstance(equipment.som, Options) else equipment.som,
            'Vibração': equipment.vibracao.value if isinstance(equipment.vibracao, Options) else equipment.vibracao,
            'Gatilho': equipment.gatilho.value if isinstance(equipment.gatilho, Options) else equipment.gatilho,
            'Lazer': equipment.lazer.value if isinstance(equipment.lazer, Options) else equipment.lazer,
            'Responsável': equipment.responsavel,
            'Email do Responvável': equipment.email,
            'UID do Responsável.': equipment.uid_responsavel,
            'Email do Resp. pela Retirada.': equipment.responsavel_retirada,
            'Email do Resp. pela Entrega.': equipment.responsavel_entrega,
            'Data de Retirada': equipment.data_retirada.strftime('%d/%m/%Y %H:%M') if isinstance(
                equipment.data_retirada, datetime) else str(equipment.data_retirada),
            'Data de Entega': equipment.data_entrega.strftime('%d/%m/%Y %H:%M') if isinstance(
                equipment.data_entrega, datetime) else str(equipment.data_entrega),
        }

    def get_items(self):
        return super().get_items(self.get_equipment_values)


eqp_hist_manager = HistRetiradaManager(HistEquipamentosRetirados, key, route='histRetirada')
eqp_hist_diver_manager = HistRetiradaManager(HistEquipamentosRetiradosDivergentes, key, route='histRetirada')

@adm_hist_ret_bp.route('/histRetirada')
def adm_hist_retirada():
    if not verify_session():
        return redirect('/')
    data_hist_ret = eqp_hist_manager.get_items()
    data_hist_ret_diver = eqp_hist_diver_manager.get_items()
    return render_template('pages/adm_hist_retirada.html', data_hist_ret=data_hist_ret, data_hist_ret_diver=data_hist_ret_diver, graph=[eqp_disp_model_graph(), eqp_ret()], labels=labels())

@adm_hist_ret_bp.route('/deletarEqpDiverRetirada', methods=['POST'])
def deletar_eqp_diver_ret():
    id_item = request.get_json().get('id')
    data = HistEquipamentosRetiradosDivergentes.query.filter_by(id=eqp_hist_diver_manager.decrypt_id(id_item)).first()
    if data:
        data_records = (HistEquipamentosRetiradosDivergentes.query
                        .order_by(HistEquipamentosRetiradosDivergentes.id.desc())
                        .filter_by(serial=data.serial)
                        .limit(2)
                        .all())
        for record in data_records:
            db.session.delete(record)
        db.session.commit()
    return 'O item foi deletado com sucesso!', 200


