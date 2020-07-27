FROM python:3.8
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt &&\
    pip install .
EXPOSE 5000
ENTRYPOINT python3 manage.py db upgrade &&\
            python3 backend/app.py
