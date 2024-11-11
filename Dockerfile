FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

RUN apt update && apt install -y --no-install-recommends build-essential \
gcc libpq-dev libc-dev pkg-config

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8080"]
