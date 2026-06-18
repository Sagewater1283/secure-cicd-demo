FROM python:3.12-slim

WORKDIR /app

COPY app ./app

ENV APP_HOST=0.0.0.0
ENV APP_PORT=8000

EXPOSE 8000

CMD ["python", "-m", "app.main"]
