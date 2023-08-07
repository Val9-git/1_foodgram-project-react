# praktikum_new_diploma

```

Данные:

```
Домен: http://vfoodgram.ddns.net/
superuser e-mail: v.lozitskiy@yandex.ru
superuser password: admin
superuser e-mail: v.lozitskiy@ya.ru
superuser password: user1user1

```

Технологи:

```
Python 3.9
Django 3.2.3
Django Rest Framework 3.12.4
Djoser 2.2.0
Gunicorn 20.1.0
```

Серверная инфраструктура:

```
Docker
PostgreSQL
Nginx
GitHub Actions
Linux Ubuntu с публичным IP
```

Как запустить проект:

```
```
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/yandex-praktikum/foodgram-project-react.git
```

```
cd backend
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

```

Авторы:

```

frontend: Яндекс Практикум;
backend, DevOps: VL;
Ревьюер: Дмитрий Кубарев
```