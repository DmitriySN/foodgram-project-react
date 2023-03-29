![This is an image](https://github.com/DmitriySN/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# Проект Foodgram
## Ссылка на тестовый сервер [Попробовать открыть](http://practikum.ddns.net/admin)

### Описание
Проект обмена рецептов для приготовления между пользователями

### Технологии

```
Django==2.2.19
django-extra-fields==3.0.2
djangorestframework==3.12.4
Pillow==8.3.1
PyJWT==2.1.0
requests==2.26.0
djoser==2.1.0
djangorestframework-simplejwt==4.8.0
django-filter==2.4.0
gunicorn==20.0.4
psycopg2-binary==2.8.6
asgiref==3.2.10
pytz==2020.1
sqlparse==0.3.1
python-dotenv==0.19.0
```

Rest API
Docker
Docker-compose

### Запуск проекта в контейнерах docker-compose

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/DmitriySN/foodgram-project-react.git
Установить переменные secrets в настройках на GitHUB
```

Запустить терминал перейти в каталог с файлом foodgram-project-react/infra/docker-compose.yaml
пересобрать контейнеры и запустить

```
docker-compose up -d --build
```

Выполнить миграции, создание суперпользователя и сгененировать статику

```
sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input
```

Создать переменные окружения в каталоге foodgram-project-react/infra/ создайте файл .env

```
SECRET_KEY='12345' # укажите секретняй ключ (установите свой)
# переменные для сервера баз данных
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```

Открыть в браузере

```
http://<ip адрес или имя домена>/admin/
```

Для восстановления Необходимо узнать id контейнера с django и залить базу

```
docker container ls -a
docker cp fixtures.json <CONTAINER ID>:/app
# Предварительно настроено имя в docker-compose можно указать или сразу так
docker cp fixtures.json api_yamdb_django:/app
docker-compose exec web python manage.py loaddata fixtures.json

```

Можно удалить дамп базы из контейнера

```
docker exec -it <CONTAINER ID> bash
# или
docker exec -it api_yamdb_django bash
rm fixtures.json
exit
```

Остановить контейнеры после проверки работоспособности

```
docker-compose down -v
```

### Для запуска на боевом сервере необходимо:

```
Остановите службу nginx чтобы высвободить 80 порт
sudo systemctl stop nginx

Установите docker и docker-compose
sudo apt install docker.io docker-compose -y

Скопируйте файлы docker-compose.yaml и nginx/default.conf и redoc.yaml из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.

Выполните копирование файла redoc в директорию статики для работы документации
sudo docker-compose exec web cp redoc.yaml /static/redoc.yaml
```

### Запуск проекта в dev-режиме

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/DmitriySN/yamdb_final
```

Войти в рабочий каталог:

```
cd yamdb_final
```

Cоздать и активировать виртуальное окружение например:

```
python -m venv venv
```

```
source venv/bin/activate - Для linux
source venv/Scripts/activate - Для windows
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r api_yamdb/requirements.txt
```

Выполнить миграции:

```
cd api_yamdb
python manage.py makemigrations
python manage.py migrate
```

По необходимости заполнить базу:
```
python manage.py loaddata ../infra/fixtures.json
```

Создать суперпользователя и статику:

```
python manage.py createsuperuser
python manage.py collectstatic
```

Запустить проект:

```
python manage.py runserver
```

Открыть в браузере

```
http://localhost:8000/admin/
```
