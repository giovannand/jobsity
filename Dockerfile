FROM python:3.8

RUN pip3 install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile
COPY ./src /app

CMD [ "python", "api.py" ]