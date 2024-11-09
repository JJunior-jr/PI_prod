# Usando a imagem oficial do Python
FROM python:3.10-slim

# Definir diretório de trabalho na imagem
WORKDIR /app

# Instalar dependências essenciais e utilitário wait-for-it
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd && apt-get install -y default-mysql-client &&\
    rm -rf /var/lib/apt/lists/*

# Copiar o arquivo de requisitos e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Expor a porta que o Flask usará
EXPOSE 5000

# Comando para iniciar a aplicação Flask
CMD ["flask", "run", "--host=0.0.0.0"]
