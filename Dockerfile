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

# 3. Use python -m to completely bypass any PATH issues
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]