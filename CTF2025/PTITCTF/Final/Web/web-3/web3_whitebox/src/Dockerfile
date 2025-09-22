FROM python:3.9-slim-buster

RUN useradd --create-home --uid 1001 --shell /bin/bash ctfuser

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R ctfuser:ctfuser /app
RUN touch database.db && chown ctfuser:ctfuser database.db
RUN chmod 444 flag.txt && chown root:root flag.txt
USER ctfuser

EXPOSE 5003


CMD ["python", "app.py"]