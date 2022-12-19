docker_compose:
	docker-compose up --build -d

create_venv:
	python3 -m venv venv

activate_venv:
	source venv/bin/activate

install_requirements:
	pip install -r requirements.txt

make_migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

load_data:
	python manage.py loaddata db.json

runserver:
	python manage.py runserver

build:
	- make docker_compose
	- make create_venv
	- make activate_venv
	- make install_requirements
	- make make_migrations
	- make migrate
	- make load_data
	- make runserver
