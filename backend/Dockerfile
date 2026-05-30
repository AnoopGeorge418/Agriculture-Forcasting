# Use a more stable python version
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependencies
COPY pyproject.toml uv.lock ./

# Install dependencies (use --no-cache to keep image small)
RUN uv sync --frozen --no-cache

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# Render uses $PORT, but defaults to 10000 if not set.
# We'll use gunicorn for better process management on Render.
# One worker is recommended for the 512MB RAM free tier.
# Use sh -c to allow environment variable expansion for $PORT
CMD ["sh", "-c", "uv run gunicorn src.Q7_fastapi_integration:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT"]
