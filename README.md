## SheepFish "Restaurant" Django test task

### 1 Installation:

Python3 should be installed

1. Clone repo `git clone https://github.com/MasterpieceElbow/sheepfish_django_test_task`
2. Build image and launch docker-compose `docker-compose up --build`
3. Install venv `python3 -m venv venv`
4. Activate venv `source venv/bin/activate`
5. Install requirements `pip install -r requirements.txt`
6. Make migrations `python manage.py makemigrations`
7. Run migrations `python manage.py migrate`
8. Load db data `python manage.py loaddata db.json`


### 2 Features

1. Asynchronous task queue with Celery and Redis
2. HTML to pdf converter using external docker service
3. Infrastructure services launched in docker-compose

### 3 Endpoints

1. Place order `POST /api/orders/`
2. Print checks `POST /api/printers/{printer_api_key}/print/`