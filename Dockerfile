FROM runpod/base:0.6.2-cuda12.1.0

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Environment defaults (MODEL_NAME must be set at runtime via RunPod env vars)
ENV MODEL_TYPE=public \
    TENSOR_PARALLEL_SIZE=1 \
    GPU_MEMORY_UTILIZATION=0.90 \
    MAX_MODEL_LEN=4096 \
    DTYPE=auto \
    QUANTIZATION="" \
    PYTHONPATH=/app

# RunPod handler entrypoint
CMD ["python", "-u", "src/handler.py"]
