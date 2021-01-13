from django.shortcuts import render
from django.http import HttpResponse

from jsonpickle import encode

from resources.db_classes import Transformer
from resources import Session



# Create your views here.
def main(request):
    session = Session() 
    try:
        transformers = session.query(Transformer).all()
        body = {"transformers": transformers}
        return HttpResponse(encode(body, unpicklable=False), content_type='application/json')
    except Exception as e:
        raise e
    finally:
        session.close()


def get_medicoes(request, id_transformer):
    session = Session()
    try:
        transformer = Transformer(id_transformer=id_transformer).get(session)
        body = dict(
                    load=transformer.load, 
                    furfural=transformer.furfural,
                    oil_quality=transformer.oil_quality,
                    dissolved_gases=transformer.dissolved_gases,
               )
        response = HttpResponse(encode(body, unpicklable=False), content_type='application/json')
        response['Accept'] = 'application/json'
        return response
    except Exception as e:
        raise e 
    finally:
        session.close()

def HI(request, id_transformer):
    pass