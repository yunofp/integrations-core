#!/bin/bash

KEYFILE_NAME="mongodb-keyfile"

if [ ! -f "$KEYFILE_NAME" ]; then
    echo "Gerando arquivo de chave..."
    openssl rand -base64 741 > "$KEYFILE_NAME"
    chmod 400 "$KEYFILE_NAME"
fi

echo "Iniciando MongoDB..."
docker-compose -f docker-compose.development.yml up -d --build

sleep 1

MONGO_CONTAINER_NAME="mongo_integrations_core"

if ! docker ps | grep -q "$MONGO_CONTAINER_NAME"; then
    echo "Container MongoDB não está em execução. Verifique os logs para possíveis erros."
    exit 1
fi

echo "Inicializando replica set..."
docker exec mongo_integrations_core /usr/bin/mongosh --username INTEGRATIONS_CORE --password INTEGRATIONS_CORE --authenticationDatabase admin --eval 'rs.initiate({_id: "rs0", members: [{_id: 0, host: "localhost:27017"}]})'

sleep 1

echo "Criando usuário..."
docker exec mongo_integrations_core /usr/bin/mongosh --username INTEGRATIONS_CORE --password INTEGRATIONS_CORE --authenticationDatabase admin --eval 'db.createUser({ user: "INTEGRATIONS_CORE", pwd: "INTEGRATIONS_CORE", roles: [ { role: "readWrite", db: "test" } ] })'
sleep 1
echo "MongoDB iniciado, replica set configurado e usuário criado."
