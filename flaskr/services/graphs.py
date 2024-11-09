from collections import Counter
from datetime import datetime, timedelta

from flaskr.models.eqp_manutencao import HistEquipamentosManutencao, EquipamentosManutencao
from flaskr.models.equipamentos import Equipamentos, Status
from flaskr.models.hist_retirada import HistEquipamentosRetirados


def get_current_week_dates():
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday() + 1)
    return [(start_of_week + timedelta(days=i)).date() for i in range(7)]


def count_per_data(data, date_field):
    filtered_dates = [
        getattr(item, date_field).date() for item in data
        if getattr(item, date_field).date() in get_current_week_dates()
    ]
    count_by_date = Counter(filtered_dates)

    return [count_by_date.get(date, 0) for date in get_current_week_dates()]


def format_dates_to_ddmmyyyy():
    return [date.strftime("%d/%m/%Y") for date in get_current_week_dates()]


def sum_eqp_man_time():
    data_eqp_man = HistEquipamentosManutencao.query.all() + EquipamentosManutencao.query.all()
    models = ["HAND HELD", "ZEBRA TC21", "HONEYWELL CT60", "HONEYWELL EDA61K"]
    count_by_model = {model: 0 for model in models}

    for item in data_eqp_man:
        item_date = getattr(item, 'data_entrada').date()
        if item_date in get_current_week_dates() and item.modelo in models:
            count_by_model[item.modelo] += 1

    return [count_by_model[model] for model in models]


def eqp_disp_model():
    data_eqp = Equipamentos.query.all()
    hand_held_disp = len([item for item in data_eqp if item.modelo == "HAND HELD" and item.status is Status.DISP])
    zebra_tc21_disp = len([item for item in data_eqp if item.modelo == "ZEBRA TC21" and item.status is Status.DISP])
    honeywell_ct60_disp = len(
        [item for item in data_eqp if item.modelo == "HONEYWELL CT60" and item.status is Status.DISP])
    honeywell_eda61k_disp = len(
        [item for item in data_eqp if item.modelo == "HONEYWELL EDA61K" and item.status is Status.DISP])
    return [hand_held_disp, zebra_tc21_disp, honeywell_ct60_disp, honeywell_eda61k_disp]


def eqp_disp_model_graph():
    hand_held_disp, zebra_tc21_disp, honeywell_ct60_disp, honeywell_eda61k_disp = eqp_disp_model()
    return (
        {'chart': {'type': 'donut', 'height': 400}, 'title': {'text': 'Eqp. disponiveis por modelo', 'align': 'center'},
         'series': [hand_held_disp, zebra_tc21_disp, honeywell_ct60_disp, honeywell_eda61k_disp],
         'colors': ['#1C7FAD', '#458E66', '#EF8F2F', '#FC6D6D'],
         'labels': ['HAND HELD', 'ZEBRA TC21', 'HONEYWELL CT60', 'HONEYWELL EDA61K'],
         'plotOptions': {'pie': {'customScale': 0.8}}})


def eqp_ret():
    data = HistEquipamentosRetirados.query.all()
    return ({
        'series': [
            {
                'name': 'Equipamentos',
                'data': count_per_data(data, 'data_retirada')
            }
        ],
        'chart': {
            'type': 'line',
            'zoom': {
                'enabled': 0
            },
            'height': 400
        },
        'colors': ['#1C7FAD'],
        'dataLabels': {
            'enabled': 1
        },
        'stroke': {
            'curve': 'straight'
        },
        'title': {
            'text': 'Eqp. retirados em função do tempo (7 dias)',
            'align': 'center'
        },
        'xaxis': {
            'categories': format_dates_to_ddmmyyyy()
        }
    })


def eqp_man():
    data = HistEquipamentosManutencao.query.all() + EquipamentosManutencao.query.all()
    return ({
        'series': [
            {
                'name': 'Equipamentos',
                'data': count_per_data(data, 'data_entrada')
            }
        ],
        'chart': {
            'type': 'line',
            'zoom': {
                'enabled': 0
            },
            'height': 400
        },
        'colors': ['#FC6D6D'],
        'dataLabels': {
            'enabled': 1
        },
        'stroke': {
            'curve': 'straight'
        },
        'title': {
            'text': 'Eqp. em manutenção em função do tempo (7 dias)',
            'align': 'center'
        },
        'xaxis': {
            'categories': format_dates_to_ddmmyyyy()
        }
    })


def eqp_man_model():
    return ({
        'series': [{
            'name': 'Equipamentos',
            'data': sum_eqp_man_time()
        }],
        'chart': {
            'type': 'bar',
            'height': 400
        },
        'colors': ['#1C7FAD', '#458E66', '#EF8F2F', '#FC6D6D'],
        'plotOptions': {
            'bar': {
                'columnWidth': '55%',
                'distributed': 'true',
            }
        },
        'dataLabels': {
            'enabled': 1
        },
        'legend': {
            'show': 0
        },
        'title': {
            'text': 'Eqp. em manutenção em função da marca (7 dias)',
            'align': 'center'
        },
        'xaxis': {
            'categories': [['HAND', 'HELD'], ['ZEBRA', 'TC21'], ['HONEYWELL', 'CT60'], ['HONEYWELL', 'EDA61K']],
        },
    })


def eqp_all():
    data_eqp_ret = HistEquipamentosRetirados.query.all()
    data_eqp_man = HistEquipamentosManutencao.query.all() + EquipamentosManutencao.query.all()
    return ({
        'series': [
            {
                'name': 'Equipamentos Retirados',
                'data': count_per_data(data_eqp_ret, 'data_retirada')
            }, {
                'name': 'Equipamentos em Manutenção',
                'data': count_per_data(data_eqp_man, 'data_entrada')
            }
        ],
        'chart': {
            'type': 'line',
            'zoom': {
                'enabled': 0
            },
            'height': 400
        },
        'colors': ['#1C7FAD', '#FC6D6D', '#458E66'],
        'dataLabels': {
            'enabled': 1
        },
        'stroke': {
            'curve': 'straight'
        },
        'title': {
            'text': 'Eqp. * em função do tempo (7 dias)',
            'align': 'center'
        },
        'xaxis': {
            'categories': format_dates_to_ddmmyyyy()
        }
    })
