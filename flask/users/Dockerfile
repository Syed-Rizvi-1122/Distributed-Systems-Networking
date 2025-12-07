FROM python:3.10

WORKDIR /app

# Copy requirements from root of repo
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Copy ONLY this microservice’s code
COPY flask/users/app.py /app/

CMD ["python", "app.py"]
