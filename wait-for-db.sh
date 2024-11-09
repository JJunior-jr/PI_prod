#!/bin/sh
# Espera até que o banco de dados esteja disponível na porta 3306
echo "Aguardando o banco de dados iniciar..."

until nc -z -v -w60 db 3306
do
  echo "Aguardando o banco de dados na porta 3306..."
  sleep 1
done

echo "Banco de dados está pronto!"
exec "$@"
