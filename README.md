# SEAI-Equipa-F
Repositório da Equipa F para desonvolvimento do projeto "Gestão de Ativos T&D" em SEAI

# Indice


- [Configuração das ferramentas](#configuração-das-ferramentas)
  - [WSL](#WSL)
  - [Ambiente virtual python/conda](#Ambiente-virtual-python/conda)
  - [Interface web](#Interface-web)
  - [Base de dados](#Base-de-dados)

# Configuração das ferramentas

## WSL
Na verdade também se pode instalar uma máquina virtual.
Os passos estão aqui: https://docs.microsoft.com/en-us/windows/wsl/install-win10


## Ambiente virtual python/conda

O conda garante que criamos todos o mesmo environment nos nossos PCs, com as mesmas bibliotecas, e tudo com as mesmas versões

Instalar ambiente virtual conda atravês do [miniconda](https://docs.conda.io/en/latest/miniconda.html) (instalação minimalista sem IDE) ou [anaconda](https://www.anaconda.com/products/individual) (instalação com navegador e IDE).

Uma maneira rápida de instalar o miniconda num sistema linux 64-bits é abrir o terminal Linux e correr:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

bash Miniconda3-latest-Linux-x86_64.sh
```

A partir daqui, se tudo estiver bem, ao abrir o terminar linux, deve aparecer o seguinte:

```bash
(base) userX@máquinaY:/dirétorio/em/que/está/aberto$
```
isto quer dizer que estamos dentro do environment **base**. O objetivo agora é criar outro environment, que vai ser o mesmo para todos. 


### Criação do ambiente
```bash
conda env create -f seai_env.yaml
```
Onde seai_env.yaml é o ficheiro de configuração no git com as dependências do ambiente.

Entrar no ambiente criado:
```bash
conda activate seai_env
```

Sair do ambiente:
```bash
conda deactivate
```

### Instalação de pacotes
Um pacote que eventualmente não esteja instalado e venha a ser preciso instalar

```bash
conda install -n seai_env pacote_a_instalar
```

### Partilhar o meu environment com o resto da equipa
Para o caso de ser preciso atualizar o ficheiro .yaml com novas bibliotecas, é assim que se cria o ficheiro
```bash
conda env export --no-build > file_name.yaml
```
Este ficheiro irá ser criado no diretório onde estão a trabalhar atualmente.

#### Nota
Para instalação de pacotes, usar de preferência o conda. Se for necessário usar o pip, certificar que é o último gestor de pacotes a instalar. Ou seja, instalar todos os pacotes do conda e só depois usar o pip. Caso sejam necessários mais pacotes do conda, é preferível criar um novo ambiente, e intalar primeiro os pacotes de conda todos novamente.

### IDE

É possível usar o Visual Studio Code (ou PyCharm) com o conda para correr mais fácilmente o programa:
  1. Com o VSCode aberto pressionar em `ctrl`+`shift`+`p` e escrever `Python: Select Interpreter`
  2. Escolher o workspace que irá usar o environment
  3. Escolher o ambiente criado anteriormente (seai_env)
  
Algumas extensões que pode ser preciso instalar no VSCode. Basta procurar as seguintes na loja de extensões, e instalar:
  1. Remote - WSL
  2. Python Extension
  3. Anaconda Extension Pack

Depois de instalar a "Remote - WSL", é possível através do VSCode, correr código no subsistema Linux, e aceder aos ficheiros que estão no WSL, em vez de ele estar a correr diretamente no Windows.

## Interface web

Para a interface web é preciso a instalação do yarn e do npm. Em ubuntu será:

```bash
sudo apt install yarn npm
```

Depois de instalado, instalar o pacote de npm:
```bash
cd src/frontend/
npm install
```

Antes de proceguir para correr o servidor web, verificar que todos os pacotes em imports foram extraídos para um package de python com pip:

```bash
cd src/imports/
pip install -e .
```

Finalemente, de preferência em dois terminais separados, correr os dois blocos de comandos para o atendimento de pedidos http:

```bash
cd src/frontend/
npm start
```

```bash
cd src/interface/
python manage.py runserver
```

Agora, a interface é acessível no port 3000 do servidor. Para a visualizar, basta colocar no endereço do browser `localhost:3000`

## Base de dados

### Docker

1. Instalar o docker Desktop (depois de estar instalado o WSL)
2. Os ficheiros relativos à base de dados estão neste momento no branch "landau" 
3. correr no diretório "db/" ->docker-compose up 
4. Assumindo que o processo do docker-compose up correu bem e ainda esta a correr, podem ir ao browser visitar http://localhost:5050/
5. user: seai@projeto.com
   password: seai_projeto
6. Onde diz servers, clicam na seta, e depois no que diz SEAI, e a password é ->postgres

### Acesso base de dados FEUP

  1. Conectar ao VPN feup
  2. Para aceder ao pgadmin aceder a este [link](https://db.fe.up.pt/phppgadmin/)
  3. User: seai
  4. pass: HEJt4ZGJc
  5. Alterar Selected_DB, no ficheiro config.json dentro da pasta resources dos imports, para "feup_db", em vez de "docker_db"
