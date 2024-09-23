FROM python:3.11-slim

WORKDIR /bot

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

ENV DATABASE=postgresql+asyncpg://postgres:holdmn@task_manager/task_manager_postgres
ENV BOT_TOKEN=7670322043:AAHw-6_DIFO2v-R47oBUcn3MC81jOO-xZHU

CMD ["python", "main.py"]