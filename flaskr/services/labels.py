from flaskr.models.equipamentos import Equipamentos, Status
from flaskr.services.graphs import eqp_disp_model


def labels():
    data = Equipamentos.query.filter_by(status=Status.DISP).count()
    hand_held_disp, zebra_tc21_disp, honeywell_ct60_disp, honeywell_eda61k_disp = eqp_disp_model()
    return [hand_held_disp, zebra_tc21_disp, honeywell_ct60_disp, honeywell_eda61k_disp, data]