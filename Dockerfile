FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY pyproject.toml README.md ./
COPY src ./src

RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir .

USER app
# 1. Make sure your actual code is copied into the container
COPY app.py ./

# Give admin rights to install the packages without cache
USER root
RUN pip install --no-cache-dir fastapi uvicorn

# 2. Force Python to print errors instantly so we aren't blind
ENV PYTHONUNBUFFERED=1

# 3. Start the server
CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "10000"]
