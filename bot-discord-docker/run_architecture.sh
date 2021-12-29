docker-compose -f docker-compose.yml up -d --build rabbitmq

docker-compose -f docker-compose.yml up -d --build donko_functions

docker-compose -f docker-compose.yml up -d --build discord_listener