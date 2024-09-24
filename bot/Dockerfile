FROM python:3.11-slim

WORKDIR /bot

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

ENV DATABASE=
ENV BOT_TOKEN=

CMD ["python", "main.py"]