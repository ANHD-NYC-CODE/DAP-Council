FROM python:3.5.3
COPY . /app
WORKDIR /app
# Latest version of pipenv, currently broken with default version
RUN pip3 install pipenv==2018.11.26
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --deploy --system
EXPOSE 8000
EXPOSE 6378