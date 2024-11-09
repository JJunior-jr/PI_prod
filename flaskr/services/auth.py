from flask import session,flash
from ..models.usuarios import Usuarios

def auth(email, password):
    data = Usuarios.query.filter_by(email=email).first()
    if data and data.verify_password(password):
        session['nome'] = data.name
        session['email']= email
        session['uid'] = data.uid
        session['status'] = data.status.value
        session['_flashes'] = None
        if data.status.value == 'Admin':
            return 'adm'
        return 'user'
    session.pop('_flashes', None)
    flash('Email ou senha incorreto', 'error')
    return False

def verify_session_adm():
    if session.get('uid') is not None:
        if session['status'] != 'Admin':
            session.pop('_flashes', None)
            flash('O usuario não tem permissão para acessar essa area', 'error')
            return False
        return True
    session.pop('_flashes', None)
    flash('Precisa estar logado para acessar o sistema', 'error')
    return False

def verify_session():
    if session.get('uid') is not None:
        return True
    session.pop('_flashes', None)
    flash('Precisa estar logado para acessar o sistema', 'error')
    return False