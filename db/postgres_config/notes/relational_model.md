# Modelo relacional DB

Transformer(<u>id_transformer</u>, age, nominal_voltage); 

Algorithm(<u>id_algorithm</u>); 

Weights(<u>id_weights</u>, H2, CH4, C2H6, C2H4, C2H2, CO, COH2, DGA_scores, oil_scores, DS_weight, IT_weight, AN_weight, WC_weight, C_weight, DF_weight, DGATC_scores, DGATC_quantity, factor, micro_water_weight, acid_value_weight, dielectric_loss_weight, breakdown_voltage_weight, algorimo1, algoritmo2);

Transformer_Algorithm_Weights(<u>#id_transformer -> Transformador</u>, <u>#id_algorithm -> Algorithm</u>, <u>#id_weights -> Weights</u>);



### Pontos a discutir

1. check contraints na tabela weights que confirma se um dos objetos é not null, os restantes pesos devem ser not null também;
2. check constraints na tabela weights para determinar a soma dos pesos;
3. comentar a tabela weights fazendo referência a que algoritmo utiliza cada parágrafo de codigo;
4. ENUM type para o algoritmo. Faz sentido?
5. As restantes tabelas a acrescentar à base de dados (data).
6. Para completarmos o diagrama de classes da base de dados precisamos de indicar os tipos das variaveis.
7. adicionar timestamps.
8. quais sao os tipos de cada variavel de manutenção? booleano?
9. tabela maintenance what is infrea-red?
10. 