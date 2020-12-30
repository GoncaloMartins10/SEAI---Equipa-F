# Como manipular os dados na DB
Esta pasta 'server' funciona como um package para trabalhar com a DB. Por trás das funções e das classes que criámos, está a biblioteca SQLAlchemy. Um script que precise de usar este package deve estar situado no diretório principal.

- [Como manipular os dados na DB](#como-manipular-os-dados-na-db)
- [Imports](#imports)
- [Adicionar na DB](#adicionar-na-db)
  - [**add(session)**](#addsession)
  - [**MixinsTables.add_batch(session,obj_list)**](#mixinstablesadd_batchsessionobj_list)
- [Atualizar valores](#atualizar-valores)
  - [**update(session)**](#updatesession)
  - [**update_batch(session,change_obj)**](#update_batchsessionchange_obj)
- [Eliminar da DB](#eliminar-da-db)
  - [**delete(session)**](#deletesession)
  - [**MixinsTables.delete_batch(session,obj_list)**](#mixinstablesdelete_batchsessionobj_list)
- [Retornar da DB (genérico)](#retornar-da-db-genérico)
  - [**get(session)**](#getsession)
  - [**get_batch(session)**](#get_batchsession)
- [Retornar medições/manutenções - Queries](#retornar-mediçõesmanutenções---queries)
- [Retornar medições/manutenções -  Funções da classe Transformer](#retornar-mediçõesmanutenções----funções-da-classe-transformer)
  - [**get_measurements(session)**](#get_measurementssession)
  - [**get_all_measurements(session)**](#get_all_measurementssession)
  - [**get_by_time_interval(session, \*\*kwargs)**](#get_by_time_intervalsession-kwargs)
  - [**get_by_interval(session, filter_list)**](#get_by_intervalsession-filter_list)

# Imports

```bash
from server.resources import Session
from server.resources.db_classes import Transformer, Weights, Furfural, Load, Oil_Quality, Dissolved_Gases, Maintenance
from server.resources.Mixins import MixinsTables

session = Session()
```
O objeto `session` é usado para manter registo das associações entre as variáveis do Python e as tabelas da DB, por isso é usado em todas as interações obrigatoriamente.

Quanto às outras classes que são importadas, cada objeto de uma dessas classes vai corresponder a uma linha da respetiva tabela.

A classe `MixinsTables` serve apenas para ir buscar a ela alguns métodos de classe que podem ser úteis, para fazer manipulações em grande escala a várias tabelas ao mesmo tempo.

# Adicionar na DB

## **add(session)**
Este metodo adiciona à DB o objeto que chama o método. Corresponde a uma linha de uma tabela. Um atributo do objeto que não esteja definido vai resultar num valor 'null', na respetiva coluna da tabela. 
### Inputs
- `session` 
### Outputs
  
### Exemplo
```bash
tr = Transformer(id_transformer="SE1", age=12)
tr.add(session)
```


## **MixinsTables.add_batch(session,obj_list)**
Adiciona à DB vários objetos de uma só vez. Podem ser objetos de classes diferentes (que vão ser guardados nas suas tabelas respetivas).

### Inputs
- `session`
- `obj_list` - uma lista de objetos, que podem ser de qualquer uma das classes importadas
### Outputs
### Exemplo
```bash
obj_list = [
    Transformer(id_transformer="SE1", age=23), 
    Furfural(id_transformer="SE1", quantity=3, datestamp='2020-12-27'), 
    Oil_Quality(id_transformer="SE1", color=2.5, datestamp='2020-12-27')
]

MixinsTables.add_batch(session,obj_list)
```

# Atualizar valores

## **update(session)**
Pesquisa o objeto pela sua primary key, e os atributos que sejam diferentes de None serão alterados nos objetos da base de dados
### Inputs
- `session` 
### Outputs
### Exemplo
```bash
# Atualizar a idade do SE1 para 20 e apagar o valor de voltagem nominal
tr = Transformer(id_transformer="SE1", age=20, nominal_voltage='delete')
tr.update(session)
```

## **update_batch(session,change_obj)**
Ver exemplo abaixo. Procura todos os objetos que sejam da classe e tenham atributos iguais a `search_obj`. Na busca, ignora atributos de `search_obj` que não estejam definidos. De seguida, em todos esses objetos, atualiza os valores dos atributos, de forma a ficarem iguais aos atributos definidos de `change_obj`. 
### Inputs
- `session` 
### Outputs
### Exemplo
```bash
search_obj = Class(arg1=x1, arg2=x2, ...)
change_obj = Class(arg3=x3, arg4=x4)
search_obj.update_batch(session, change_attr=change_obj)
```

# Eliminar da DB 

## **delete(session)**
Pesquisa o objeto pelo seu primary key, e remove-o da base de dados
### Inputs
- `session` 
### Outputs
### Exemplo
```bash
tr = Transformer(id_transformer="SE1")
tr.delete(session)
```

## **MixinsTables.delete_batch(session,obj_list)**
Este metodo pesquisa cada obj (através da sua primary key) que esteja na lista obj_list e apaga-os da base de dados
### Inputs
- `session`
- `obj_list` - lista com os objetos a serem apagados
### Outputs
### Exemplo
```bash
obj_list = [
    Transformer(id_transformer="SE1"), 
    Furfural(id_furfural_measurement="SE1"), 
]
MixinsTables.delete_batch(session,obj_list)
```


# Retornar da DB (genérico)
Para qualquer tabela da DB

## **get(session)**
Através da primary key definida no objeto que chama o método, é retornado o objeto completo.
### Inputs
- `session` 
### Outputs
- `obj` - um objeto da mesma classe do objeto que chamou o método, mas este objeto tem os atributos todos preenchidos conforme o que encontrou na DB
### Exemplo
```bash
tr = Transformer(id_transformer="SE1")
tr = tr.get(session)

print(tr.age)
>> 12
```

## **get_batch(session)**
Este metodo pesquisa os objetos que tenham os atributos do objeto self criado, e retorna-os numa lista.
### Inputs
- `session` 
### Outputs
- `obj_list` - lista com todos os objetos que tenham os atributos procurados
### Exemplo
```bash
# Pesquisa os transformadores que tenham 12 anos
tr = Transformer(age=12)
obj_list = tr.get_batch(session)

print(obj_list[0].id_transformer)
>> 'SE1'
```

# Retornar medições/manutenções - Queries

1. Tanto quanto nos interessa perceber, em SQLAlchemy uma `query` comporta-se como uma lista de objetos da mesma classe (uma lista de linhas da tabela `Furfural`, por exemplo). 
2. Esta lista pode ser filtrada pela função `filter()`, com base em qualquer regra que dê jeito definir.
3. Esta lista pode ser ordenada com base num atributo (coluna) qualquer, com a funão `order_by()`
4. Podemos saber o número de linhas de qualquer query com a função `count()`

```bash
# Aceder ao impact_index da primeira linha da tabela de manutenções
myquery = session.query(Maintenance)
print(myquery[0].impact_index)
>>-2

# Agora vamos filtrar a query que temos, para ficar apenas com as manutenções do último ano
myquery = myquery.filter(Maintenance.datestamp >= '2020-01-01')
print(myquery[0].datestamp)
>>'2020-03-14' # em qualquer posição, será uma data que obedece ao filtro

# E agora filtrar ainda mais a query para ficar só com as medições do SE5
myquery = myquery.filter(Maintenance.id_transformer == 'SE5')
print(myquery[7].datestamp,'  ',myquery[7].id_transformer)
>> '2020-08-13  SE5' 

# Finalmente, pode dar jeito ter a certeza que a query (a lista) está ordenada, por exemplo, pelo datestamp
myquery = myquery.order_by(Maintenance.datestamp)        # ordem ascendente
myquery = myquery.order_by(Maintenance.datestamp.desc()) # ordem descendente

# Exatamente a mesma query (lista), podia ser retornada apenas numa só linha:
myquery = session.query(Maintenance).filter(Maintenance.datestamp >= '2020-01-01').filter(Maintenance.id_transformer == 'SE5').order_by(Maintenance.datestamp.desc())

# Adicionalmente, podemos saber o número de manutenções que aconteceram a partir de 2020 no SE5, com a função count()
print(myquery.count())
>> 4
```

Para o caso de serem úteis, estão já escritas algumas funções:


# Retornar medições/manutenções -  Funções da classe Transformer
> Nota: quem diz medições, diz manutenções

##  **get_measurements(session)**
Procura todas as medições de um dado transformador que constam numa das tabelas. O transformardor selecionado corresponde ao objeto que chama o método.
### Inputs
- `session`
- `table` - nome da classe que define a tabela 
### Outputs
- obj_list - lista de objetos (linhas) do transformador e da tabela selecionados
### Exemplo
```bash
trs=Transformer(id_transformer='SE2')
obj_list = trans.get_measurements(session,'Furfural')

print(obj_list[0].quantity)
>> 0.4 # quantidade de furfural na primeira medição que consta do SE2
```

## **get_all_measurements(session)**
Procura todas as medições de um dado transformador, mas não se cinge a uma tabela: retorna para todas. O retorno é um dicionário que permite aceder adicionalmente à tabela desejada.
### Inputs
- `session` 
### Outputs
- `dict_obj_list` - dicionário em que as keys são os nomes das tabelas, e os values são as respetivas listas de objetos. 
### Exemplo
```bash
trans=Transformer(id_transformer='SE2')
res=trans.get_all_measurements(session)

print(res['Furfural'][0].quantity)
>> 0.4
```

## **get_by_time_interval(session, \*\*kwargs)**
Semelhante ao `get_all_measurements(session)`, mas permite a definição de uma data mínima e máxima para os objetos (linhas de tabela) que são retornados. Estes limites são usados para filtrar TODAS as tabelas. É possível só definir um dos limites, ou não definir nenhum: nesse caso retorna um dicionário de query que não chegam a ser filtradas.
### Inputs
- `session` 
- `mindate` - Opcional. Data mínima que será usada para filtar a query
- `maxdate` - Opcional. Data máxima que será usada para filtar a query
### Outputs
- `dict_query` - dicionário em que as keys são os nomes das tabelas, e os values são as respetivas queries filtradas. Como explicado acima, uma query comporta-se exatamente como uma lista de objetos, quando tentamos ler os dados. 
### Exemplo
```bash
trans=Transformer(id_transformer='SE2')
res=trans.get_by_time_interval(session,mindate='2002-11-01',maxdate='2020-11-30')

print(res['Furfural'][0].quantity)
>> 0.4
print(res['Furfural'][0].datestamp)
>> '2004-05-12'
```

## **get_by_interval(session, filter_list)**
Semelhante ao `get_all_measurements(session)`, mas permite a definição de limites para qualquer atributos das medições, que serão usados para filtrar as queries.
### Inputs
- `session`
- `filter_list` - lista de dicionários que permite definir limites para qualquer atributo (coluna) que se queira filtrar. A estrutura está exemplificada abaixo. Cada dicionário corresponde a uma ou duas filtragens (consoante são definidos 1 ou 2 limites). É obrigatório que o primeiro valor do dicionário corresponda ao nome da coluna pela qual se pretende filtrar.
### Outputs
- `dict_query` - dicionário em que as keys são os nomes das tabelas, e os values são as respetivas queries filtradas. Como explicado acima, uma query comporta-se exatamente como uma lista de objetos, quando tentamos ler os dados. 
### Exemplo
```bash
filt = [
    {'column': 'quantity',  'min': 0.5},
    {'column': 'h2',        'max': 0.5},
    {'column': 'datestamp', 'min': '2000-11-01', 'max': '2010-11-30'}
]
trs=Transformer(id_transformer='SE3')
dict_query=trs.get_by_interval(session,filt)
```