FROM python:3.10-alpine

WORKDIR /app

# Install only essential dependencies for MySQL
RUN apk add --no-cache \
    mariadb-connector-c-dev \
    build-base \
    pkgconfig

COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . /app/

# Create non-root user
RUN adduser -D -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]