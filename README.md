# SEAI-Equipa-F
Repositório da Equipa F para desonvolvimento do projeto "Gestão de Ativos T&D" em SEAI


# WSL
Na verdade também se pode instalar uma máquina virtual.
Os passos estão aqui: https://docs.microsoft.com/en-us/windows/wsl/install-win10


# Ambiente virtual python/conda
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


## Criação do ambiente
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

## Instalação de pacotes
Um pacote que eventualmente não esteja instalado e venha a ser preciso instalar

```bash
conda install -n seai_env pacote_a_instalar
```

## Partilhar o meu environment com o resto da equipa
Para o caso de ser preciso atualizar o ficheiro .yaml com novas bibliotecas, é assim que se cria o ficheiro
```bash
conda env export --no-build > file_name.yaml
```
Este ficheiro irá ser criado no diretório onde estão a trabalhar atualmente.

### Nota
Para instalação de pacotes, usar de preferência o conda. Se for necessário usar o pip, certificar que é o último gestor de pacotes a instalar. Ou seja, instalar todos os pacotes do conda e só depois usar o pip. Caso sejam necessários mais pacotes do conda, é preferível criar um novo ambiente, e intalar primeiro os pacotes de conda todos novamente.

## IDE

É possível usar o Visual Studio Code (ou PyCharm) com o conda para correr mais fácilmente o programa:
  1. Com o VSCode aberto pressionar em `ctrl`+`shift`+`p` e escrever `Python: Select Interpreter`
  2. Escolher o workspace que irá usar o environment
  3. Escolher o ambiente criado anteriormente (seai_env)
  
Algumas extensões que pode ser preciso instalar no VSCode. Basta procurar as seguintes na loja de extensões, e instalar:
  Remote - WSL
  Python Extension
  Anaconda Extension Pack

Depois de instalar a "Remote - WSL", é possível através do VSCode, correr código no subsistema Linux, e aceder aos ficheiros que estão no WSL, em vez de ele estar a correr diretamente no Windows.

# Docker

1. Instalar o docker Desktop (depois de estar instalado o WSL)
2. Os ficheiros relativos à base de dados estão neste momento no branch "landau" 
3. correr no diretório "db/" ->docker-compose up 
4. Assumindo que o processo do docker-compose up correu bem e ainda esta a correr, podem ir ao browser visitar http://localhost:5050/
5. user: seai@projeto.com
   password: seai_projeto
6. Onde diz servers, clicam na seta, e depois no que diz SEAI, e a password é ->postgres
