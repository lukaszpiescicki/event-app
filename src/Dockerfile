FROM python:latest
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml .
RUN pip install -r requirements.txt
COPY patient .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]