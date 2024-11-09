from flask import Blueprint, render_template, redirect
from ..services.auth import verify_session
from . import eqp_man_manager
from ..services.graphs import eqp_disp_model_graph
from ..services.labels import labels

user_eqp_man_bp = Blueprint('user_eqp_man_bp', __name__)

@user_eqp_man_bp.route('/userEqpManutencao')
def user_eqp_manutencao():
    if not verify_session():
        return redirect('/')
    data_eqp_man = eqp_man_manager.get_items()
    return render_template('pages/user_eqp_manutencao.html', data_eqp_man=data_eqp_man, graph=[eqp_disp_model_graph()], labels=labels())