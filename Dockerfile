FROM python:3-alpine

WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY songs2slides songs2slides

CMD ["gunicorn", "-b", "0.0.0.0:5000", "songs2slides:create_app()"]
