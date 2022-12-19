## SheepFish "Restaurant" Django test task

### 1 Installation:

Python3 should be installed

1. Clone repo `git clone https://github.com/MasterpieceElbow/sheepfish_django_test_task`
2. If you have `make` installed run `make build` or follow instructions 3-9
3. Build image and launch docker-compose `docker-compose up --build`
4. Install venv `python3 -m venv venv`
5. Activate venv `source venv/bin/activate`
6. Install requirements `pip install -r requirements.txt`
7. Make migrations `python manage.py makemigrations`
8. Run migrations `python manage.py migrate`
9. Load db data `python manage.py loaddata db.json`

Go to `127.0.0.1:8000/admin` and auth with `admin:admin`

### 2 Features

1. Asynchronous task queue with Celery and Redis
2. HTML to pdf converter using external docker service
3. Infrastructure services launched in docker-compose

### 3 Endpoints

1. Place order `POST /api/orders/`
2. Print checks `POST /api/printers/{printer_api_key}/print/`

Swagger OpenAPI doc specified in `api.yaml`
