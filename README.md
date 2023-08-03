# praktikum_new_diplom
### Как запустить проект:
Данные:
Домен: http://vfoodgram.ddns.net/
superuser e-mail: v.lozitskiy@yandex.ru
superuser password: admin
superuser e-mail: v.lozitskiy@ya.ru
superuser password: user1user1

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
