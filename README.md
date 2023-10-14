### t3_fastApi

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Bogdan-Malina/t3_fastApi.git
```

```
cd t3_fastApi
```

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
poetry run python create_base.py
```

### Автор
Данил Воронин https://github.com/Bogdan-Malina

