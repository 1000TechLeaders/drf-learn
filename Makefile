.PHONY: install_dev
install_dev:
	python -m pip install -r requirements.txt
	pre-commit install


.PHONY: start_docker_compose
start_docker_compose:
	cd tests && docker compose up


.PHONY: test
test:
	pytest tests --cov --cov-report term-missing


.PHONY: run_dev
run_dev:
	python manage.py runserver 0:8085


.PHONY: superuser
superuser:
	python manage.py createsuperuser


.PHONY: migrate
migrate:
	python manage.py migrate
