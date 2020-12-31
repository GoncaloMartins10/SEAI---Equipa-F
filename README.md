# SEAI-Equipa-F
Repositório da Equipa F para desonvolvimento do projeto "Gestão de Ativos T&D" em SEAI


# Ambiente virtual python/conda
Instalar ambiente virtual conda atravês do [miniconda](https://docs.conda.io/en/latest/miniconda.html) (instalação minimalista sem IDE) ou [anaconda](https://www.anaconda.com/products/individual) (instalação com navegador e IDE).

Depois de instalado, em windows, correr o `anaconda prompt` para poder correr os comandos. Em linux não deve ser necessário. 

## Criação do ambiente
```bash
conda env create -f seai_env.yaml
```
Onde seai_env.yaml é o ficheiro de configuração no git com as dependências do ambiente.

Para criar este ficheiro, instalar os pacotes necessários e usar:
```bash
conda env export > file_name.yaml
```
Este ficheiro irá ser criado no diretório onde estão a trabalhar atualmente.

Entrar no ambiente criado:
```bash
conda activate seai_env
```

Sair do ambiente:
```bash
conda deactivate
```

## Instalação de pacotes
```bash
conda install -n seai_env pacote_a_instalar
```

### Nota
Para instalação de pacotes, usar de preferência o conda. Se for necessário usar o pip, certificar que é o último gestor de pacotes a instalar. Ou seja, instalar todos os pacotes do conda e só depois usar o pip. Caso sejam necessários mais pacotes do conda, é preferível criar um novo ambiente, e intalar primeiro os pacotes de conda todos novamente.

## IDE

É possível usar o Visual Studio Code (ou PyCharm) com o conda para correr mais fácilmente o programa:
  1. Com o VSCode aberto pressionar em `ctrl`+`shift`+`p` e escrever `Python: Select Interpreter`
  2. Escolher o workspace que irá usar o environment
  3. Escolher o ambiente criado anteriormente (seai_env)~

# Acesso base de dados FEUP

  1. Conectar ao VPN feup
  2. Para aceder ao pgadmin aceder a este [link](https://db.fe.up.pt/phppgadmin/)
  3. User: seai
  4. pass: HEJt4ZGJc
  5. É ainda preciso alterar e acrescentar um ficheiro de configuração para usar esta base de dados