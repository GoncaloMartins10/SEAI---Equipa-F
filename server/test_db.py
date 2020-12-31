#-----------------------------------------------------------------------#
# Este ficheiro serve para popular a base de dados com dados aleatórios #
#                  É preciso que a DB esteja vazia                      #
#-----------------------------------------------------------------------#

from resources.db_classes import Transformer, Furfural, Oil_Quality, Load, Dissolved_Gases, Maintenance
from resources import Session
from resources.Mixins import MixinsTables
from numpy.random import rand,randint

session = Session()

MixinsTables.delete_all(session)

def rand_date():
    year = randint(1995,2020)
    month = randint(1,12)
    day = randint(1,28)
    return str(year)+'-'+str(month)+'-'+str(day)

trs   = [Transformer(id_transformer="SE"+str(i+1), age=i+10 ) for i in range(8)]
loads = [Load(id_transformer="SE"+str(j+1), power_factor=rand(), load_factor=rand(),datestamp=rand_date()) for j in range(8) for i in range(20)]
furfs = [Furfural(id_transformer="SE"+str(j+1),quantity=rand(),datestamp=rand_date()) for j in range(8) for i in range(20)]
oils  = [Oil_Quality(id_transformer="SE"+str(j+1),breakdown_voltage=rand(),water_content=rand(),acidity=rand(),color=rand(),interfacial_tension=rand(),datestamp=rand_date()) for j in range(8) for i in range(20)]
disgs = [Dissolved_Gases(id_transformer="SE"+str(j+1),h2=rand(),ch4=rand(),c2h6=rand(),c2h4=rand(),c2h2=rand(),co=rand(),coh2=rand(),datestamp=rand_date()) for j in range(8) for i in range(20)]

MixinsTables.add_batch(session, trs)
MixinsTables.add_batch(session, loads)
MixinsTables.add_batch(session, furfs)
MixinsTables.add_batch(session, oils)
MixinsTables.add_batch(session, disgs)

