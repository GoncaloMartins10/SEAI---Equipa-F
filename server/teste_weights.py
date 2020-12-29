from resources import Session
from resources.db_classes import Transformer,Weights,Furfural,Load,Oil_Quality,Dissolved_Gases

session=Session()

# ------ Exemplo get_measurements --------
# trans=Transformer(id_transformer='SE2')
# res = trans.get_measurements(session,'Furfural')
# print (res[0].quantity)

# ---- Exemplo get_all_measurements() -----
# trans=Transformer(id_transformer='SE2')
# res=trans.get_all_measurements(session)
# print(res['Furfural'][0].quantity)

# ---- Exemplo get_by_time_interval() -----
# trans=Transformer(id_transformer='SE2')
# res=trans.get_by_time_interval(session,mindate='2002-11-01',maxdate='2020-11-30')
# print(res['Furfural'][0].datestamp)
# print(res['Furfural'].count) # Nr de entradas de Furfural que são selecionadas pela query

# ---- Exemplo get_by_interval() -----
# filt = [
#     {'column': 'quantity',  'min': 0.5},
#     {'column': 'h2',        'max': 0.5},
#     {'column': 'datestamp', 'min': '2000-11-01', 'max': '2010-11-30'}
# ]
# trans=Transformer(id_transformer='SE3')
# res=trans.get_by_interval(session,filt)
# print(res['Furfural'][0].datestamp)
