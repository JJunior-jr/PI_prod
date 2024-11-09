from flask import Blueprint
from cryptography.fernet import Fernet

from ..services.graphs import eqp_disp_model_graph, eqp_ret, eqp_man, eqp_man_model, eqp_all
from ..services.labels import labels

key = Fernet(Fernet.generate_key())

main = Blueprint('main', __name__)

from .auth_route import *
from .adm_eqp_route import *
from .adm_user_route import *
from .adm_hist_ret_route import *
from .adm_eqp_man_route import *
from .user_eqp_route import *
from .user_eqp_man_route import *

main.register_blueprint(auth_bp)
main.register_blueprint(adm_eqp_bp)
main.register_blueprint(adm_user_bp)
main.register_blueprint(adm_hist_ret_bp)
main.register_blueprint(adm_eqp_man_bp)
main.register_blueprint(user_eqp_bp)
main.register_blueprint(user_eqp_man_bp)

@main.route('/')
def index():
    flashes = session.pop('_flashes', None)
    session.clear()
    match flashes:
        case [('error', 'Email ou senha incorreto')]:
            session['_flashes'] = flashes
        case [('error', 'O usuario não tem permissão para acessar essa area')]:
            session['_flashes'] = flashes
        case [('error', 'Precisa estar logado para acessar o sistema')]:
            session['_flashes'] = flashes
        case [('error', 'Se o email estiver correto, foi enviado as intruções para recuperar o acesso')]:
            session['_flashes'] = flashes
        case _:
            session['_flashes'] = None
    return render_template('index.html')

@main.route('/dashboardAdm')
def adm_dashboard():
    if not verify_session_adm():
        return redirect('/')
    return render_template('pages/adm_dashboard.html', graph=[eqp_disp_model_graph(), eqp_ret(), eqp_man(), eqp_man_model(), eqp_all()], labels=labels())

@main.route('/dashboard')
def dashboard():
    if not verify_session():
        return redirect('/')
    return render_template('pages/user_dashboard.html', graph=[eqp_disp_model_graph()], labels=labels())