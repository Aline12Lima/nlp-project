# ============================================
# STAGE 1: Builder — instala dependências
# ============================================
FROM python:3.11-slim AS builder

WORKDIR /build

# Dependências de sistema necessárias apenas para build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas requirements para aproveitar cache do Docker
COPY requirements.txt .

# Instala torch CPU-only (muito menor) primeiro, depois o resto
RUN pip install --no-cache-dir --user \
    --index-url https://download.pytorch.org/whl/cpu \
    torch==2.3.0 && \
    pip install --no-cache-dir --user \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt


# ============================================
# STAGE 2: Runtime — imagem final enxuta
# ============================================
FROM python:3.11-slim

WORKDIR /app

# Apenas o que precisamos em runtime (sem compiladores)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia pacotes Python instalados no builder
COPY --from=builder /root/.local /root/.local

# Garante que scripts instalados estão no PATH
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copia o código da aplicação
COPY . .

# Cria pasta para modelos (será populada em runtime via volume)
RUN mkdir -p /app/models

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
