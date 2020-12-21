from flask import Blueprint
from resources.response import build_response

from .Models import Transformer
from resources.db_classes import Transformer_Algorithm_Weights


mod_Transformer = Blueprint('mod_transformer', __name__)


@mod_Transformer.route('/', methods=['GET'])
def transformer_measurements():
    # ainda temos de definir o que pomos aqui
    return build_response({}, status_code=400)

@mod_Transformer.route('/measurements', methods=['GET'])
def get_measurements():
    # ainda temos de definir o que pomos aqui
    return build_response({}, status_code=400)
