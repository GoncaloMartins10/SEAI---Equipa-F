from resources.db_classes import Transformer, Furfural, Oil_Quality, Load, Dissolved_Gases
from resources import Session
from resources.Mixins import MixinsTables

session = Session()

trs = [Transformer(id_transformer="SE"+str(i+1), age=i+10 ) for i in range(8)]
MixinsTables.add_batch(session, trs)

loads = [Load(id_transformer="SE"+str(j+1)) for j in range(8) for i in range(20)]
MixinsTables.add_batch(session, loads)
furfs = [Furfural(id_transformer="SE"+str(j+1)) for j in range(8) for i in range(20)]
MixinsTables.add_batch(session, furfs)
oils  = [Oil_Quality(id_transformer="SE"+str(j+1)) for j in range(8) for i in range(20)]
MixinsTables.add_batch(session, oils)
disgs = [Dissolved_Gases(id_transformer="SE"+str(j+1)) for j in range(8) for i in range(20)]
MixinsTables.add_batch(session, disgs)
