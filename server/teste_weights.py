from resources import Session
from resources.db_classes import Transformer,Weights,Furfural,Load,Oil_Quality,Dissolved_Gases
#from resources.weights.Models import Weights

session=Session()
# test=Weights(id_weights=19, h2=55)
# test.add(session)

# res=Weights(id_weights=19)
# res.get(session)
# print('H2:  ',res.h2)

# new=Transformer(id_transformer='SE2')
# new.add(session)

# addition=Furfural(id_transformer='SE2',quantity=7,datestamp='2020-12-12')
# e = addition.add(session)

# addition=Furfural(id_transformer='SE2',quantity=6,datestamp='2020-11-11')
# e = addition.add(session)

# addition=Furfural(id_transformer='SE2',quantity=5,datestamp='2020-10-10')
# e = addition.add(session)

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
# res=trans.get_by_time_interval(session,mindate='2020-11-01',maxdate='2020-11-30')
# print(res['Furfural'][0].datestamp)

# ---- Exemplo get_by_interval() -----
# listkwargs = [
# 	{
# 		'column':'quantity',
# 		'min':7,
# 	},
# 	{
# 		'column': 'datestamp',
# 		'min':'2020-11-01',
#         'max':'2021-11-30'
# 	},
# ]
# trans=Transformer(id_transformer='SE2')
# res=trans.get_by_interval(session,listkwargs)
# print(res['Furfural'][0].datestamp)
