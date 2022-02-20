FROM python:3.8

RUN pip3 install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile
COPY . /app

CMD [ "python", "./src/producer.py" ]

