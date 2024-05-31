# Проект HW №38 

## Описание проекта

Подготовка и размещение веб-приложения Django на GitHub и деплой на сервер TimeWeb

## Установка и запуск проекта

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/Demek07/HW_38.git
    cd HW_38
    ```

2. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    source venv/bin/activate  # для Windows: venv\Scripts\activate
    ```

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4. Скопируйте файл `.env.example` и переименуйте его в `.env`:
    ```bash
    cp .env.example .env
    ```

5. Откройте файл `.env` и заполните следующие переменные окружения:
	- SECRET_KEY=ВВЕДИТЕ_ДЖАНГО_СЕКРЕТНЫЙ_КЛЮЧ
	- EMAIL_HOST_PASSWORD=ВВЕДИТЕ_ПАРОЛЬ_ОТ_ПОЧТЫ
	- EMAIL_HOST=ВВЕДИТЕ_ХОСТ_ПОЧТЫ
	- EMAIL_PORT=ВВЕДИТЕ_ПОРТ_ПОЧТЫ
	- EMAIL_HOST_USER=ВВЕДИТЕ_ВАШ_ЕМЕЙЛ

6. Примените миграции:
    ```bash
    python manage.py migrate
    ```

7. Создайте суперпользователя для доступа к админ-панели Django:
    ```bash
    python manage.py createsuperuser
    ```

8. Загрузите DUMP базы:
    ```bash
	python manage.py loaddata dump.json
    ```

9. Запустите сервер разработки:
    ```bash
    python manage.py runserver
    ```

