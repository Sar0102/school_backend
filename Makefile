make-migrations:
	python manage.py makemigrations

run:
	python manage.py runserver 0.0.0.0:9000

start-server:
	python manage.py runserver 0.0.0.0:9000 && python manage.py migrate
