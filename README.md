
# Projeto Integrador - Controle de Estoque

Este projeto utiliza Flask com um banco de dados MariaDB para gerenciar o controle de estoque.
- Atenção: Clonar o repositório

## Pré-requisitos instalação local direto na maquina

1. **MariaDB**: Certifique-se de ter o MariaDB instalado em sua máquina.
2. **Banco de Dados**: Crie um banco de dados chamado `pi_project` no MariaDB.
3. **Python**: Verifique se o Python 3 está instalado.

## Configuração do Ambiente

1. **Criar Ambiente Virtual**:
   ```bash
   python -m venv <nome_do_ambiente>
   ```

2. **Ativar Ambiente Virtual**:
   ```bash
   source <nome_do_ambiente>/bin/activate
   ```

3. **Instalar Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuração do Banco de Dados

1. **Criar Migrations** (para versionamento do banco de dados):
   ```bash
   flask --app flaskr db init
   ```
   
2. **Migrar Estrutura**:
   ```bash
   flask --app flaskr db migrate -m "Criando tabelas"
   ```

3. **Aplicar Atualizações**:
   ```bash
   flask --app flaskr db upgrade
   ```

## Executando a Aplicação

Para iniciar a aplicação, utilize o comando:

```bash
python run.py
```

## Inserir a senha do banco de dados

Para inserir a senha do banco de dados, acesse o arquivo config.py localizado na pasta config e insira a senha

```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:<senha do banco>@localhost/pi_project'
```

## Pré-requisitos instalação via Docker

- Sistema operacional Linux (ex.: Ubuntu, Debian).
- Acesso root ou permissão `sudo` para executar comandos administrativos.
- Clone do repositório

## 1. Instalação do Docker

### Passo 1: Atualizar o Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### Passo 2: Instalar Pacotes Necessários
```bash
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
```

### Passo 3: Adicionar a Chave GPG do Docker
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

### Passo 4: Adicionar o Repositório do Docker
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Passo 5: Instalar o Docker
```bash
sudo apt update
sudo apt install docker-ce -y
```

### Passo 6: Verificar a Instalação do Docker
```bash
docker --version
```

### Passo 7: Habilitar e Iniciar o Docker
```bash
sudo systemctl start docker
sudo systemctl enable docker
```
# Projeto Integrador - Controle de Estoque

3. **Aplicar Atualizações**:
   ```bash
   flask --app flaskr db upgrade
   ```

## Executando a Aplicação

Para iniciar a aplicação, utilize o comando:

```bash
python run.py
```

## Inserir a senha do banco de dados

Para inserir a senha do banco de dados, acesse o arquivo config.py localizado na pasta config e insira a senha

```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:<senha do banco>@localhost/pi_project'
```

## Pré-requisitos instalação via Docker

- Sistema operacional Linux (ex.: Ubuntu, Debian).
- Acesso root ou permissão `sudo` para executar comandos administrativos.
- Clone do repositório

## 1. Instalação do Docker

### Passo 1: Atualizar o Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### Passo 2: Instalar Pacotes Necessários
```bash
## 2. Instalação do Docker Compose

### Passo 1: Baixar o Docker Compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -oP '(?<="tag_name": ")[^"]*')/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

### Passo 2: Dar Permissão de Execução
```bash
sudo chmod +x /usr/local/bin/docker-compose
```

### Passo 3: Verificar a Instalação do Docker Compose
```bash
docker-compose --version
```

## 3. Configuração de Permissão para Usuário (Opcional)

Para evitar o uso do `sudo` ao executar comandos Docker, adicione seu usuário ao grupo Docker.

```bash
sudo usermod -aG docker ${USER}
```

> **Nota:** Após executar esse comando, faça logout e login novamente para que as permissões sejam aplicadas.

---

## 4. Testando a Instalação

Para verificar se tudo está funcionando corretamente, execute o seguinte comando:

```bash
docker run hello-world
```

Esse comando baixa uma imagem de teste e exibe uma mensagem confirmando que o Docker está funcionando.

## 5. Inserir a senha do banco de dados

Para inserir a senha do banco de dados, acesse o arquivo config.py localizado na pasta config e insira a senha, deixar conforme abaixo:

```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:<senha do banco>@db/pi_project'
```

## 6. Executar o ambiente

- docker-compose up --build

## 7. Acessar a aplicação

- http://127.0.0.1:5000
- usuario: admin@admin.com
- senha: admin


