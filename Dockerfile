FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt && pip install gunicorn
COPY . /code/

RUN python3 manage.py collectstatic

EXPOSE 8000

ENTRYPOINT ["sh", "/code/docker-entrypoint.sh"]
CMD serve