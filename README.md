![CI workflow](https://github.com/dangerousmonk/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# Foodgram - сервис для публикации рецептов
## Доступен по адресу: http://dangerousmonk.hopto.org/


Сервис позволяет пользователям просматривать рецепты любимых блюд, а также публиковать собственные.
При регистрации пользователь указывает свой email, который будет использоваться при авторизации.
![foodgram-main](https://user-images.githubusercontent.com/74264747/130495494-1eb4c107-209a-40cd-a4ac-12f40762725b.jpg)
![foodgram-main2](https://user-images.githubusercontent.com/74264747/130495522-0bf86788-1c17-4186-af86-a2c6853262ad.jpg)

Зарегестрированные пользователи могут подписываться на авторов рецептов или добавлять рецепты в корзину, в избранное.
Есть возможность фильтрации рецептов по тегам, поиск по началу названия ингредиента при добавлении или редактировании рецепта.


![recipe-detail](https://user-images.githubusercontent.com/74264747/130495561-d3193e9d-c759-4b00-8562-0f2ef4e37ce3.jpg)


## Запуск проекта локально
- Склонировать проект и перейти в папку проекта

```bash
git clone https://github.com/dangerousmonk/foodgram-project-react
cd foodgram-project-react
```
- Установить Python 3.8.3 в случае если он не установлен
- Установить и активировать виртуальное окружение, или создать новый проект в PyCharm

```bash
python3 -m venv venv
source venv\bin\activate
```

- Установить зависимости из файла **requirements.txt**
 
```bash
pip install -r requirements.txt
``` 
- В папке с файлом manage.py выполнить команды:

```bash
python manage.py makemigrations
python manage.py migrate
```
- Создать пользователя с неограниченными правами:

```bash
python manage.py createsuperuser
```
- Запустить web-сервер на локальной машине:

```bash
python manage.py runserver --settings=foodgram.settings-dev
```



## Docker инструкции
- Установить Docker и получить образ

```
docker pull dangerousmonk/foodgram-project-react:latest
```

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
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=someuser@gmail.com
EMAIL_HOST_PASSWORD=secretpassword
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


## TODO
- Добавить выгрузку списка покупок в pdf вместо txt
- Обновить и переработать тесты
- Оптимизация запросов
- Добавить locale файлы
- Добавить отправку email уведомления
- Добавить схему БД