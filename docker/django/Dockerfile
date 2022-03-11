FROM python:3.10.1

RUN pip install pipenv

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/
COPY ./Pipfile ./
COPY ./Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile
COPY ./ ./
RUN python ./manage.py collectstatic --noinput

EXPOSE 8080

ENTRYPOINT ["gunicorn", "--reload", "--bind", "0.0.0.0:8080", "app.wsgi:application" ]