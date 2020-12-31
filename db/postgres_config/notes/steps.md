
1. Sistema operativo Linux (WSL, ou qualquer distribuição Linux)

2. Instalar o docker

   > https://docs.docker.com/docker-for-windows/wsl/

3. Instalar o docker-compose

   > https://docs.docker.com/compose/install/

4. No diretorio do repositorio /db

   - \>docker-compose up

5. Assumindo que o passo anterior correu como esperado, falta determinar o ID do container que corre o serviço do postgres

   - \>docker ps

6. Entrar no processo do postgres (é nos dado um terminal desse processo)

   - \>docker exec \-it [CONTAINER ID] bash

7. Entrar no serviço postgres dentro do processo:

   - psql -U postgres

8. Montar a base de dados no serviço do postgres:
    1. No caso de ser a primeira vez que inciamos a base de dados:
        \>CREATE DATABASE seai
        \>\\c seai
        \>CREATE SCHEMA ges_ativos
    2. Correr o resto do ficheiro database/create_tables.sql:
        - IMPORTANTE: so é necessário correr depois da 3a linha de codigo... As duas primeiras pertencem ao passo anterior.
