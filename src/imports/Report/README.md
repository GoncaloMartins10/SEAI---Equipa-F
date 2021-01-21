# Gerar relatório

Os relatórios são gerados e colocados na pasta static/doc

Código exemplo para gerar uníco relatório:

```python
from imports.Report import generate_report, get_data_for_report

data = get_data_for_report(transformer)
generat_report = generate_report(transformer, data)
```

Código exemplo para gerar relatórios para todos os transformadores:

```python
from imports.Report import generate_all_reports

generate_all_reports()
```