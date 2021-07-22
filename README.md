# Foodgram - сервис для публикации рецептов
## Доступен по адресу: http://dangerousmonk.hopto.org/


## Запуск проекта для отладки
- Склонировать проект и перейти в папку проекта

```bash
git clone https://github.com/dangerousmonk/gfoodgram-project-react
cd infra_sp2
```
- Установить Python 3.9. в случае если он не установлен
- Установить Docker

```
docker pull dangerousmonk/foodgram-project-react:v1.1
```


## Docker инструкции
Проект можно развернуть используя контейнеризацию с помощью Docker  
Параметры запуска описаны в `docker-compose.yml`.

При запуске создаются три контейнера:

 - контейнер базы данных **db**
 - контейнер приложения **backend**
 - контейнер web-сервера **nginx**

Для развертывания контейнеров необходимо:


- Создать и сохранить переменные окружения в **.env** файл, образец ниже
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram_exmpl
POSTGRES_USER=user
POSTGRES_PASSWORD=12345
POSTGRES_DB=yamdb #имя БД которое возьмет образ postgres
DB_HOST=db
DB_PORT=5432
```

- Запустить docker-compose

```bash
docker-compose up
```
- Выполнить миграции и подключить статику

```bash
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
```
- Создать superuser

```bash
docker-compose exec backend python manage.py createsuperuser
```

- Пользователь для доступа в административную часть
- Второй пользователь
```bash
admin@gmail.com
admin12345

piterparker@gmail.com
piter12345
```
