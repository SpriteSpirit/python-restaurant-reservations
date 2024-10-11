# Сайт для бронирования столиков в ресторане (Fullstack)

### Описание задачи:

Необходимо создать сайт для бронирования столиков в ресторане. Сайт должен быть сверстан и подключен к админке. Для
выполнения задачи необходимо использовать Django и Bootstrap. Сайт должен содержать основные разделы, необходимые для
бронирования столиков и управления бронированиями.

### Задача:

1. Сверстать сайт для бронирования столиков.
2. Подключить сайт к админке Django.
3. Использовать Bootstrap для создания адаптивного и привлекательного интерфейса.
4. Подготовить финальную [презентацию](https://drive.google.com/file/d/1E7HRn_vfF2KpK_tz6sVTQhV1OKUDo5VW/view?usp=sharing) для защиты

### Функционал сайта:

1. **Главная страница**:
    - [x] Описание ресторана.
    - [x] Перечень предоставляемых услуг.
    - [x] Контактная информация.
    - [x] Форма для обратной связи.
2. **Страница "О ресторане"**:
    - [x] История ресторана.
    - [x] Миссия и ценности.
    - [x] Команда.
3. **Страница бронирования**:
    - [x] Форма для бронирования столика.
    - [x] Просмотр доступности столиков.
    - [x] Подтверждение бронирования.
4. **Личный кабинет**:
    - [x] Регистрация и авторизация пользователей.
    - [x] Просмотр истории бронирований.
    - [x] Управление текущими бронированиями (изменение, отмена).
5. **Админка**:
    - [x] Управление пользователями.
    - [x] Управление бронированиями.
    - [x] Управление контентом сайта (тексты, изображения и т.д.).

### **Технологии**

1. **Фреймворк**:
    - Использовать фреймворк Django для реализации проекта.
2. **База данных**:
    - Использовать PostgreSQL для хранения данных.
3. **Фронтенд**:
    - Использовать Bootstrap для создания адаптивного интерфейса.
4. **Контейнеризация**:
    - Использовать Docker и Docker Compose для контейнеризации приложения.
5. **Документация**:
    - В корне проекта должен быть файл README.md с описанием структуры проекта и инструкциями по установке и запуску.
6. **Качество кода**:
    - Соблюдать стандарты PEP8.
    - Весь код должен храниться в удаленном Git репозитории.

### **Установка и запуск**

**Предварительные условия:**

* Python 3.11
* PostgreSQL
* Poetry
* Redis
* Celery
* Bootstrap

### Информация

Главное приложение проекта - **config**.

 ```  
    restaurant_reservations/
    ├── config/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── celery.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── restaurant/
    │   ├── migrations/
    │   ├── templates/
    │       ├── restaurant/
    │   ├── templatetags/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── tasks.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── users/
    │   ├── fixtures/
    │   ├── managements/
    │   │   ├── commands/
    │   │   │   ├── __init__.py
    │   │   │   └── csu.py
    │   │   └── __init__.py
    │   ├── migrations/
    │   ├── templates/
    │       ├── users/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── media/
    ├── static/
    ├── .env_example
    ├── .gitignore
    ├── Dockerfile
    ├── docker-compose.yaml
    ├── .dockerignore
    ├── manage.py
    ├── poetry.lock
    ├── poetry.toml
    └── README.md
```

### Установка:

1. **Клонирование репозитория:**

```powershell
   git clone <репозиторий_GitHub>
   cd <название_репозитория>
```

2. **Установка poetry:**

```bash 
   pip install poetry
```

3. **Установка зависимостей:**

```bash 
   poetry install
```

4. **Настройка переменных окружения:**

Создайте файл .env в корне проекта и заполните его переменными по шаблону **.env_example:**

```
DATABASE_URL=<URL_для_подключения_к_PostgreSQL>
SECRET_KEY=<секретный_ключ>
...
```

5. **Создание базы данных:**

```bash 
  python manage.py migrate
```

6. **Создание администратора:**

```bash 
  python manage.py csu
```

7. **Запуск сервера разработки:**

```bash 
   python manage.py runserver
```

8. **Запуск Celery (для отложенных задач Windows):**

```bash
   celery -A config worker -l info -P gevent
```

9. **Запуск Flower (для мониторинга Celery задач):**

```bash
   celery -A config flower --port=5555
```

### PEP8

**Для формирования отчета при помощи flake8-html выполните команду:**

```bash
  flake8 --format=html --ignore=migrations/,venv/,E501 --htmldir=flake8_report ./
```

**--format=html** - параметр, указывающий на тип формата отчета

**--ignore=migrations/,venv,E501** - параметр принимает: игнорируемые директории, файлы, коды ошибок

**--htmldir=flake8_report ./** - параметр для создания директории с отчетом

**./** - это корневая директория проекта для создания папки flake8_report

**index.html** - файл с отчетом

### Развертывание с помощью Docker и Docker Compose

Этот проект можно легко развернуть с помощью Docker и Docker Compose. Для этого необходимо установить Docker и Docker
Compose на вашей системе.

1. **Создайте файлы Dockerfile и docker-compose.yaml в корне проекта:**

#### Dockerfile

- описывает шаги для создания образа Docker для приложения Django, используя Poetry для управления зависимостями:

```dockerfile
FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.8.3 \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache, artifacts}

COPY . .

RUN apt-get update && apt-get install -y procps netcat curl && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y netcat

```

#### Docker Compose

Файл `docker-compose.yaml` описывает сервисы, необходимые для запуска приложения, включая Django, PostgreSQL, Redis и
Celery:

```yaml
services:
  db:
    image: postgres:16
    restart: always
    env_file:
      - .env
    environment:
      POSTGRES_DB: ${DATABASE_NAME}
      POSTGRES_USER: ${DATABASE_USER}
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - ./db_data:/var/lib/postgresql/data
    healthcheck:
      test: [ "CMD-SHELL", "pg_isready -U ${DATABASE_USER} -d ${DATABASE_NAME}" ]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:alpine
    restart: always
    ports:
      - "6380:6379"
    healthcheck:
      test: [ "CMD", "redis-cli", "ping" ]
      interval: 5s
      timeout: 5s
      retries: 5

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    restart: always
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy

  celery_worker:
    build: .
    command: celery -A config worker -l info
    restart: always
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis
      - web

  celery_beat:
    build: .
    command: celery -A config beat -l info -S django
    restart: always
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis
      - web

volumes:
  db_data:
    driver: local

```

2. **Запустите контейнеры Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   Этот процесс создаст и запустит все необходимые контейнеры. Для запуска в фоновом режиме используйте:

   ```bash
   docker-compose up --build -d
   ```

4. **Примените миграции Django:**

 ```bash
   docker-compose exec app python manage.py migrate
   ```

5. **Приложение будет доступно по адресу `http://localhost:8000`.**

## Остановка и очистка

- **Остановить контейнеры:**

  ```bash
  docker-compose down
  ```

- **Очистить тома данных (если используются):**

  ```bash
  docker-compose down -v
  ```
- **Очистка неиспользуемых данных Docker**
   ```bash
   docker system prune -af
   ```
- **Очистка неиспользуемых данных Docker + также удаление неиспользуемых томов**
   ```bash
   docker system prune -af --volumes
   ```

## Примечания

- Убедитесь, что у вас установлен Docker и Docker Compose.
- Измените `your_password` в файле `.env` на свой пароль для PostgreSQL.
- Вы можете остановить контейнеры с помощью команды `docker-compose down`.
- Убедитесь, что порты, используемые в `docker-compose.yaml`, свободны на вашем хосте.
- Для доступа к базе данных PostgreSQL внутри контейнера
  используйте `docker-compose exec db psql -U your_db_user your_db_name`.
- Для просмотра логов Celery или Django используйте `docker-compose logs -f celery` или `docker-compose logs -f app`.

## Дополнительно

- **Резервное копирование данных:** Регулярно создавайте резервные копии данных PostgreSQL, если это необходимо.
- **Обновления:** Время от времени обновляйте образы Docker и зависимости проекта для безопасности и производительности.
- **Poetry:** Убедитесь, что версия Poetry, указанная в Dockerfile, совпадает с той, что используется в вашем проекте
  для избежания конфликтов зависимостей.

### **Автор**

```Халуева Ангелина||Sprite_Spirit```
