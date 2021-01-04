from imports.HI_calculation.health_index import calculate_all_transformers
from imports.resources import Session

session = Session()
calculate_all_transformers(session, 4)