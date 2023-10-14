### t3_fastApi

### Как запустить проект:

В папке infra создайте файл .env с переменными:
```
DB_PORT
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
```
Из папки infra выполните:
```
docker-compose up --build
```
Зайдите в контейнер t3_fastApi
```
docker container ls

docker exec -it <CONTAINER ID> bash
```
Заполните базу данных
```
python create_base.py
```

### Автор
Данил Воронин https://github.com/Bogdan-Malina

