FROM python:3.8.12-slim-bullseye

WORKDIR /backend

RUN pip install poetry==1.1.12 gunicorn==20.1.0
ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root

COPY manager .

ENTRYPOINT ["gunicorn", "manager.wsgi"]
CMD ["--bind", "0.0.0.0:8000"]
