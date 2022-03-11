stop:
	docker-compose down
build:
	docker-compose build
start: build
	docker-compose --env-file .env up -d
	docker-compose exec django python manage.py makemigrations
	docker-compose exec django python manage.py migrate
	docker-compose exec django python manage.py collectstatic --noinput
admin:
	docker-compose exec django python manage.py createsuperuser