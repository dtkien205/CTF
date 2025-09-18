FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=registration.settings
ENV PYTHONUNBUFFERED=1

RUN useradd -m ctf

RUN python manage.py makemigrations
RUN python manage.py migrate

RUN mv flag.txt /flag-$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1).txt && \
    chmod 644 /flag-*.txt

RUN apt-get update && apt-get install -y sqlite3 && \
    sqlite3 db.sqlite3 "UPDATE auth_user SET password='$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 128 | head -n 1)' WHERE id=1;"

RUN chown -R ctf:ctf /app

EXPOSE 8000

USER ctf
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]