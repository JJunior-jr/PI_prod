from flask import Blueprint, render_template, request, redirect
from ..models.eqp_manutencao import HistEquipamentosManutencao, EquipamentosManutencao
from ..services.auth import verify_session_adm
from ..models.usuarios import Usuarios, Status
from ..services.model_manager import ModelManager
from . import key, set_new_password

adm_user_bp = Blueprint('adm_user_bp', __name__)

class UserManager(ModelManager):
    def _get_empty_dict(self):
        return {
            'id': '',
            'nome': '',
            'email': '',
            'UID': '',
            'status': ''
        }

    @staticmethod
    def get_user_values(user):
        return {
            'nome': user.name,
            'email': user.email,
            'UID': user.uid,
            'status': user.status.value if isinstance(user.status, Status) else user.status
        }

    def get_items(self):
        return super().get_items(self.get_user_values)

    @staticmethod
    def build_user_data(form):
        status = form['status']
        status = Status.ADM if status == 'Admin' else Status.USER

        unique_fields = {
            'uid': form['uid'],
            'email': form['email']
        }

        field_values = {
            'name': form['nome'],
            'uid': form['uid'],
            'email': form['email'],
            'status': status
        }

        return unique_fields, field_values

user_manager = UserManager(Usuarios, key, route='admUsuarios')

@adm_user_bp.route('/admUsuarios')
def adm_usuarios():
    if not verify_session_adm():
        return redirect('/')
    data_users = user_manager.get_items()
    return render_template('pages/adm_usuarios.html', data_users=data_users)

@adm_user_bp.route('/editarUser', methods=['POST'])
def editar_user():
    id_item = request.form['id']
    data = Usuarios.query.filter_by(id=user_manager.decrypt_id(id_item)).first()
    unique_fields, field_values = user_manager.build_user_data(request.form)
    data_hist_man = HistEquipamentosManutencao.query.filter_by(uid_resp_ocorr=data.uid, email_resp_ocorr=data.email).all()
    data_man = EquipamentosManutencao.query.filter_by(uid_resp_ocorr=data.uid, email_resp_ocorr=data.email).all()
    for item in data_hist_man + data_man:
        item.uid_resp_ocorr = field_values['uid']
        item.email_resp_ocorr = field_values['email']
    if user_manager.update_item(id_item, unique_fields, field_values):
        return redirect('/admUsuarios')
    return redirect('/admUsuarios')

@adm_user_bp.route('/resgistrarUser', methods=['POST'])
def resgistrar_user():
    unique_fields, field_values = user_manager.build_user_data(request.form)
    if user_manager.add_item(unique_fields, field_values):
        set_new_password(unique_fields['email'], 'Bem vindo!')
        return redirect('/admUsuarios')
    return redirect('/admUsuarios')

@adm_user_bp.route('/deletarUser', methods=['POST'])
def deletar_user():
    id_item = request.get_json().get('id')
    if user_manager.remove_item(id_item):
        return 'O item foi deletado com sucesso!', 200
    return 'Erro ao deletar o item.', 400
