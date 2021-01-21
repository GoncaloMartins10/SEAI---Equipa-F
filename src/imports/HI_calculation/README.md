# Utilização dos algoritmos

Os métodos dos cálculos de indice de vida estão mapeados da seguinte forma:

1. Hydro-Québec
2. Kinectrics-based model
3. Methodology based on multi-feature factor
4. Methodology for transformer condition assessment

Como exemplo o cálculo do indice de vida usando o método Hydro-Québec

```python
from imports.HI_algorithm import calculate_all_transformers, calculate_for_transformer
from imports.resources import Session

session = Session()

populate_database = True
method = 1

# Para vários transformadores
results = calculate_all_transformers(session, method, populate_database)

result = calculate_for_transformer(session, transformer, method, populate = True)

session.close()

```

O valor do argumento populate_database está predefinido para verdadeiro, não sendo preciso defini-lo caso seja pretendida esta função