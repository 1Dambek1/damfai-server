FROM python


WORKDIR /app


COPY req.txt .
RUN   pip install -r req.txt
COPY . .


CMD gunicorn  src.app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

