# Multi-stage Dockerfile for Project Forge
# Optimized for Windows and Linux compatibility

# Stage 1: Base Python environment
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create app directory
WORKDIR /app

# Stage 2: Dependencies installation
FROM base as dependencies

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Application
FROM base as application

# Copy installed dependencies from previous stage
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Copy application code
COPY project_forge/ /app/project_forge/
COPY streamlit_ui/ /app/streamlit_ui/
COPY streamlit_app.py /app/
COPY README.md /app/

# Create output directory for generated READMEs
RUN mkdir -p /app/output

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose Streamlit port
EXPOSE 8501

# Default command (can be overridden in docker-compose)
CMD ["streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
