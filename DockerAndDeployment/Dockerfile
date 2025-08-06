# ---- Builder Stage ----
FROM python:3.11-slim AS builder

# Install uv package manager
RUN pip install --no-cache-dir uv

# Set workdir
WORKDIR /app

# Copy pyproject.toml and install dependencies
COPY pyproject.toml ./
RUN uv pip install --system --no-cache-dir --prod

# Copy application code
COPY app ./app

# ---- Runtime Stage ----
FROM python:3.11-slim AS runtime

# Create non-root user
RUN useradd -m appuser
WORKDIR /app

# Copy dependencies and app from builder
COPY --from=builder /app /app

# Copy Alembic and Nginx config if needed
COPY alembic alembic
COPY nginx nginx

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/appuser/.local/bin:$PATH"

# Switch to non-root user
USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Entrypoint
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]