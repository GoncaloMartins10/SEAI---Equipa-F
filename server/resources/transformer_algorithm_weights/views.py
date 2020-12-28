from flask import Blueprint
from resources.response import build_response

from .Models import Transformer_Algorithm_Weights
from resources.db_classes import Transformer


mod_TransformerAlgorithmWeights = Blueprint('mod_TransformerAlgorithmWeights', __name__)

@mod_TransformerAlgorithmWeights.route('/', methods=['PUT'])
def transformer_algorithm_weights_update():
    # ainda temos que definir o que acontece aqui
    return build_response({}, status_code=400)

