"""Configurações compartilhadas para testes pytest."""
import os

# Configura variáveis de ambiente antes de importar a aplicação
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("HF_HOME", "./models")
