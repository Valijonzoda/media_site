FROM python:3.10g

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

CMD celery -A media_site worker --loglevel=info & python manage.py runserver 0.0.0.0:8000
