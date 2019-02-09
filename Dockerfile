FROM python:3.6.5
COPY . /app/
WORKDIR /app/
# Latest version of pipenv, currently broken with default version
RUN pip3 install pipenv==2018.11.26
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
RUN pipenv install --deploy --system
COPY ./docker-entrypoint.sh /

EXPOSE 8000
RUN chmod +x /app/docker-entrypoint.sh
ENTRYPOINT ["/app/docker-entrypoint.sh"]
