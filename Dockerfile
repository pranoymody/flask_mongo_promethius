FROM python:2.7

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

HEALTHCHECK CMD curl --fail http://localhost:5000/ || exit 1

CMD ["python", "app.py"]
