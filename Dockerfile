FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./src/requirements.txt /app/src/requirements.txt

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install --no-cache-dir redis azure-monitor-opentelemetry python-dotenv uv

COPY . /app/

# Change to src directory and run uv sync
WORKDIR /app/src
RUN uv sync --frozen
WORKDIR /app

# Make entrypoint.sh executable
RUN chmod +x /app/src/entrypoint.sh

CMD ["python", "-m", "uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
