FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY flask/products/app.py /app/

CMD ["python", "app.py"]
