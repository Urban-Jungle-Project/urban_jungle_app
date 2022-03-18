FROM python:slim

RUN useradd urban_jungle

WORKDIR /home/urban_jungle

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql cryptography

COPY app app
COPY migrations migrations
COPY urban_jungle.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP urban_jungle.py

RUN chown -R urban_jungle:urban_jungle ./
USER urban_jungle

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]