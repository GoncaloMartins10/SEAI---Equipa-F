from flask import Flask

from resources.transformer.views import mod_Transformer
from resources.transformer_algorithm_weights.views import mod_TransformerAlgorithmWeights
from resources.health_index.views import mod_HealthIndex


app = Flask(__name__)

app.register_blueprint(mod_Transformer, url_prefix='/api/transformer')
app.register_blueprint(mod_TransformerAlgorithmWeights, url_prefix='/api/transformer_algorithm_weights')
app.register_blueprint(mod_HealthIndex, url_prefix='/api/health_index')
