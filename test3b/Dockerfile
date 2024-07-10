FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .


RUN chmod -R 755 /app

CMD ["python", "main.py"]
