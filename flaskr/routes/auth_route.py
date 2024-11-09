import string
import random
from flask_mail import Message
from flask import Blueprint, request, redirect, session, flash, render_template
from flaskr import db, mail
from flaskr.models.eqp_manutencao import HistEquipamentosManutencao, EquipamentosManutencao
from flaskr.models.usuarios import Usuarios

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    from ..services.auth import auth
    auth = auth(request.form['email'], request.form['senha'])
    if auth == 'adm':
        return redirect('/dashboardAdm')
    elif auth == 'user':
        return redirect('/dashboard')
    else:
        return redirect('/')


@auth_bp.route('/editarMeuUsuario', methods=['POST'])
def edit_meu_user():
    # Essa com certeza foi a função mais porca que já fiz nessa aplicação e olha que tem muitas, mas essa supera todas, mas funciona...
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    confirmar_senha = request.form['confirmar-senha']
    if senha != confirmar_senha:
        session.pop('_flashes', None)
        flash('As senhas estão divergentes', 'error')
    else:
        data = Usuarios.query.filter_by(uid=session['uid']).first()
        if senha != '': data.set_password(senha)
        if Usuarios.query.filter_by(email=email).first() is None and email != session['email']:
            data_man = HistEquipamentosManutencao.query.filter_by(email_resp_ocorr=data.email).all()
            data_eqp = EquipamentosManutencao.query.filter_by(email_resp_ocorr=data.email).all()
            for item in data_man + data_eqp:
                item.email_resp_ocorr = email
            data.email = email
            data.nome = nome
            db.session.commit()
            session['email'] = email
            session['_flashes'] = None
        elif email != session['email']:
            session.pop('_flashes', None)
            flash('Esse email já está sendo usando por outro usuario', 'error')
        else:
            session['_flashes'] = None
        db.session.commit()
    session['message_route'] = request.referrer
    return redirect(request.referrer)

def set_new_password(email, subject):
    caracteres = string.ascii_letters + string.digits
    senha = ''.join(random.choice(caracteres) for _ in range(8))
    data = Usuarios.query.filter_by(email=email).first()
    if data is not None:
        data.set_password(senha)
        msg = Message(subject, recipients=[data.email])
        msg.html = render_template("pages/email_template.html", nome=data.name, senha=senha)
        mail.send(msg)
        db.session.commit()
        return True
    return False

@auth_bp.route('/esqueciSenha', methods=['POST'])
def esqueci_senha():
    email = request.form['email']
    set_new_password(email, 'Recuperar a senha')
    session.pop('_flashes', None)
    flash('Se o email estiver correto, foi enviado as intruções para recuperar o acesso', 'error')
    return redirect('/')