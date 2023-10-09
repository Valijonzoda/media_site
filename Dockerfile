FROM python:3.10g

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

CMD python manage.py runserver 0.0.0.0:8000
