FROM python:3.10
ENV PYTHONUNBUFFERED=1
#ENV POETRY_VIRTUALENVS_CREATE=0
WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .
RUN pip3 install poetry
RUN poetry install
COPY . .
CMD ["python", "src/manage.py", "runserver", "8000"]
