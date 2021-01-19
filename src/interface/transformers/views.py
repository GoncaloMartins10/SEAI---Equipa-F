from django.shortcuts import render
from django.http import HttpResponse

from jsonpickle import encode

from resources.db_classes import Transformer
from resources import Session

from .Report.report import generate_report, generate_all_reports



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
        return HttpResponse(encode(body, unpicklable=False), content_type='application/json')
    except Exception as e:
        raise e 
    finally:
        session.close()

def HI(request, id_transformer):
    session = Session()
    try:
        health_indices = Transformer(id_transformer=id_transformer).get(session).health_index
        return HttpResponse(encode(health_indices, unpicklable=False), content_type='application/json')
    except Exception as e:
        raise e
    finally:
        session.close()


def report(request, id_transformer):
    session = Session()
    try:
        transformer = Transformer(id_transformer=id_transformer).get(session)
        data = {
            "Load and Power Factor": transformer.load, 
            "Furfural": transformer.furfural,
            'Oil Quality':transformer.oil_quality,
            'Dissolved Gases':transformer.dissolved_gases,
            'Overall Condition': transformer.overall_condition,
            'Health Index': transformer.health_index
        }
        generate_report(transformer, data)
    except Exception as e:
        raise e
    finally: 
        session.close()

    pass