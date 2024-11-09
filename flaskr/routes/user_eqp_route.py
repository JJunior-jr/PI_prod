from datetime import datetime
from flask import Blueprint, render_template, request, redirect, session, flash
from .adm_eqp_route import EquipmentoManager
from flaskr import db
from ..models.equipamentos import Equipamentos, Status, Options
from ..models.hist_retirada import HistEquipamentosRetirados, HistEquipamentosRetiradosDivergentes
from ..models.usuarios import Usuarios
from ..services.auth import verify_session
from . import key
from ..services.graphs import eqp_disp_model_graph
from ..services.labels import labels

user_eqp_bp = Blueprint('user_eqp_bp', __name__)
eqp_manager = EquipmentoManager(Equipamentos, key, route='equipamentosUser')
@user_eqp_bp.route('/equipamentosUser')
def user_equipamentos():
    if not verify_session():
        return redirect('/')
    data_eqp = eqp_manager.get_items()
    return render_template('pages/user_equipamentos.html', data_eqp=data_eqp, graph=[eqp_disp_model_graph()], labels=labels())

@user_eqp_bp.route('/retirarEqp', methods=['POST'])
def retirar_eqp():
    id_item = request.form['id']
    uid = request.form['uid-do-responsavel']
    data_usr = Usuarios.query.filter_by(uid=uid).first()
    data = Equipamentos.query.filter_by(id=eqp_manager.decrypt_id(id_item)).first()
    if data_usr is not None:
        data.status = Status.INDISP
        new_eqp = HistEquipamentosRetirados(serial=data.serial,wifi_ip=data.wifi_ip, modelo=data.modelo,
                                            responsavel=data_usr.name, email=data_usr.email, uid_responsavel=uid, responsavel_retirada=session['email'],
                                            data_retirada=datetime.now(), coldre=data.coldre, alca=data.alca,
                                            touch=data.touch, som=data.som, vibracao=data.vibracao,
                                            gatilho=data.gatilho, lazer=data.lazer)
        db.session.add(new_eqp)
        db.session.commit()
        session['id_item'] = None
        session['_flashes'] = None
    else:
        session.pop('_flashes', None)
        session['id_item'] = f"'{data.serial}'"
        session['route'] = 'equipamentosUser'
        flash('O UID do usuario não está cadastrado.', 'error')
    return redirect('/equipamentosUser')

@user_eqp_bp.route('/entregarEqp', methods=['POST'])
def entregar_eqp():
    id_item = request.form['id']
    data_eqp = Equipamentos.query.filter_by(id=eqp_manager.decrypt_id(id_item)).first()
    data = HistEquipamentosRetirados.query.order_by(HistEquipamentosRetirados.id.desc()).filter_by(serial=data_eqp.serial).first()
    data.data_entrega = datetime.now()
    data.responsavel_entrega = session['email']
    new_eqp_data = {
        'serial': data.serial,
        'wifi_ip': data.wifi_ip,
        'modelo': data.modelo,
        'responsavel': data.responsavel,
        'email': data.email,
        'uid_responsavel': data.uid_responsavel,
        'responsavel_retirada': data.responsavel_retirada,
        'responsavel_entrega': session['email'],
        'data_retirada': data.data_retirada,
        'data_entrega': datetime.now(),
        'coldre': request.form['coldre'],
        'alca': request.form['alca'],
        'touch': request.form['touch'],
        'som': request.form['som'],
        'vibracao': request.form['vibracao'],
        'gatilho': request.form['gatilho'],
        'lazer': request.form['lazer']
    }

    divergent = False
    labels = ['coldre', 'alca', 'touch', 'som', 'vibracao', 'gatilho', 'lazer']
    for label in labels:
        d = Options.SIM if request.form[label] == 'Sim' else Options.NAO
        if d != getattr(data, label):
            divergent = True
            break

    if divergent:
        new_eqp_diver_last = HistEquipamentosRetiradosDivergentes(**new_eqp_data)
        data_dict = {key: value for key, value in data.__dict__.items() if key != '_sa_instance_state' and key != 'id'}
        new_eqp_diver = HistEquipamentosRetiradosDivergentes(**data_dict)
        for label in labels:
            setattr(data, label, new_eqp_data[label])
            setattr(data_eqp, label, new_eqp_data[label])
        db.session.add(new_eqp_diver_last)
        db.session.add(new_eqp_diver)
    data_eqp.status = Status.DISP
    db.session.commit()
    return redirect('/equipamentosUser')