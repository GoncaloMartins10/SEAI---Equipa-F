from imports.HI_calculation.algorithms.method_4 import Method_4
from imports.HI_calculation.algorithms.method_1 import Method_1
from imports.resources.db_classes import Transformer
from imports.resources import Session
session=Session()


# result_1 = Method_4().calculate_for_transformer(Transformer(id_transformer="SE4").get(session))
result_1 = Method_1().calculate_for_transformer(Transformer(id_transformer="SE2").get(session))
hi_list = [res.hi for res in result_1]
print(hi_list)