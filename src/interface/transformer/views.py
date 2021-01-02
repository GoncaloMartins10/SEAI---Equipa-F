from django.http import HttpResponse
from django.shortcuts import render
from resources.db_classes import Transformer
from resources import Session


def index(request):
    session = Session()
    transformers = session.query(Transformer).all()
    context = {
            'transformers': transformers
    }
    return render(request, 'transformer/index.html', context)


def get_transformer(request, id_transformer):
    session = Session()
    test = Transformer(id_transformer = id_transformer).get(session)
    context = {
        'furfural': test.furfural,                  #
        'load': test.load,                          #
        'dissolved_gases': test.dissolved_gases,    # 
        'oil_quality': test.oil_quality,            #
        'maintenance': test.maintenance             # 
    }
    return HttpResponse("Hello World")
    # return render(request, 'transformer/transformer.html', context)
