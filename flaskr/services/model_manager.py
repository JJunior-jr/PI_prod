from flaskr import db
from flask import flash, session
import json
import base64

from flaskr.models.usuarios import Usuarios


class ModelManager:
    def __init__(self, model, key, route):
        self.model = model
        self.key = key
        self.route = route

    def encrypt_id(self, value):
        value_bytes = str(value).encode()
        encrypted_value = self.key.encrypt(value_bytes)
        return base64.urlsafe_b64encode(encrypted_value).decode()

    def decrypt_id(self, encrypted_value):
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_value)
        decrypted_value = self.key.decrypt(encrypted_bytes)
        return decrypted_value.decode()

    def _check_duplicates(self, unique_fields, instance=None):
        for field, value in unique_fields.items():
            existing = self.model.query.filter_by(**{field: value}).first()
            if existing and (instance is None or existing != instance):
                session.pop('_flashes', None)
                session['id_item'] = None
                session['route'] = self.route
                flash(f'O {field} já está cadastrado.', 'error')
                return False
        return True

    def add_item(self, unique_fields, field_values, status_map=None, option_map=None):
        if not self._check_duplicates(unique_fields):
            return False

        new_item = self.model(**field_values)

        if self.model is Usuarios:
            new_item.set_password('mudarSenha')

        db.session.add(new_item)
        db.session.commit()
        session['_flashes'] = None
        return True

    def remove_item(self, encrypted_id):
        item_id = self.decrypt_id(encrypted_id)
        data = self.model.query.filter_by(id=item_id).first()

        db.session.delete(data)
        db.session.commit()
        return True

    def update_item(self, encrypted_id, unique_fields, field_values, status_map=None, option_map=None):
        item_id = self.decrypt_id(encrypted_id)
        data = self.model.query.filter_by(id=item_id).first()

        if not self._check_duplicates(unique_fields, instance=data):
            session['id_item'] = f'"{getattr(data, next(iter(unique_fields.keys())))}"'
            session['route'] = self.route
            return False
        for field, value in field_values.items():
            setattr(data, field, value)

        db.session.commit()
        session['_flashes'] = None
        return True

    def get_items(self, value_mapper):
        data = self.model.query.order_by(self.model.id.desc()).all()
        dict_data = [
            {
                'id': self.encrypt_id(item.id),
                **value_mapper(item)
            }
            for item in data
        ]

        if not data:
            dict_data = [self._get_empty_dict()]
        json_data = json.dumps(dict_data, ensure_ascii=False, indent=4)
        return json_data

    def _get_empty_dict(self):
        raise NotImplementedError("Subclasses devem implementar o método _get_empty_dict.")
