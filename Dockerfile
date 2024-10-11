FROM python:3.12
WORKDIR /app


COPY req.txt .
RUN pip install --no-cache-dir -r req.txt
COPY . .

CMD gunicorn  src.app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

