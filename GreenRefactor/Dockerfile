# ============================================================
# STAGE 1: Builder — compile Python packages
# ============================================================
FROM python:3.13-slim AS builder

WORKDIR /build
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ gfortran libopenblas-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /build/
# Pip upgrade only (setuptools and msgpack are handled here)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ============================================================
# STAGE 2: Runtime — assemble and PURGE unwanted packages
# ============================================================
FROM python:3.13-slim AS runtime

# Install runtime dependencies for scipy/numpy and utilities
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends libgfortran5 libopenblas0-pthread curl tar gzip bash && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /usr/local/lib/python3.13/site-packages/*

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app
COPY . /app/

# Start the FastAPI server
CMD ["python", "-m", "uvicorn", "Backend.api:app", "--host", "0.0.0.0", "--port", "8000"]