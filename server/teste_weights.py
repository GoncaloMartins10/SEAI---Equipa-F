from resources import Session
from resources.db_classes import Weights
#from resources.weights.Models import Weights

session=Session()
#test=Weights(id_weights=19, h2=55)
#test.add(session)

res=Weights()
res.get(session,h2=54)
print(res.id_weights)