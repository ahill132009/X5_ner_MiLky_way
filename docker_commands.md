# доступные образы (получить image_id)
docker images 

# сделать образ
docker build -t rubert-ner-api_v1 .  

# запустить терминал внутри образа
docker run -it --rm image_id /bin/bash  

# запустить сервис образа
docker run -d --name ner-service -p 8000:8000 rubert-ner-api_v1

# остановить и удалить сервис образа
docker stop ner-service
docker rm ner-service

# удалить образ
docker rmi image_id

# логи
docker logs ner-service  
