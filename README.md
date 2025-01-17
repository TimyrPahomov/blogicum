# Blogicum

Проект **Blogicum** позволяет пользователям публиковать посты.

Для **всех** пользователей реализованы следующие возможности:
- просмотр списка постов на главной и отдельных постов;
- просмотр страниц пользователей;
- создание аккаунта;
  
**Авторизованным** пользователям дополнительно доступны:
- вход в систему под своим логином и паролем и выход из системы;
- создание, редактирование и удаление собственных постов;
- создание, редактирование и удаление комментариев к постам;

## Содержание
- [Технологии](https://github.com/TimyrPahomov/blogicum#технологии)
- [Локальный запуск](https://github.com/TimyrPahomov/blogicum#локальный-запуск)
- [Автор](https://github.com/TimyrPahomov/blogicum#автор)

## Технологии
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)

## Локальный запуск
1. Необходимо клонировать репозиторий и перейти в него:

```sh
git clone https://github.com/TimyrPahomov/blogicum.git
cd blogicum/
```

2. Далее нужно создать и активировать виртуальное окружение:

```sh
python -m venv venv
source venv/Scripts/activate
```

3. Обновить пакетный менеджер и установить зависимости из файла _requirements.txt_:

```sh
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Затем следует перейти в директорию с файлом _manage.py_ и выполнить миграции:

```sh
cd blogicum/
python manage.py migrate
```

5. Наконец, запустить проект:

```sh
python manage.py runserver
```

## Автор
[Пахомов Тимур](<https://github.com/TimyrPahomov/>)