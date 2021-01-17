from imports.resources import Session
from imports.HI_calculation.health_index import calculate_all_transformers

session=Session()

for i in [1,2,3,4]:
    print(f"==== METHOD {i} ====")
    result = calculate_all_transformers(session, i)