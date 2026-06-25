# NLP Portfolio API

> Pipeline de NLP com FastAPI, HuggingFace e Docker — projeto de portfólio em construção.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![Tests](https://img.shields.io/badge/tests-6%20passed-brightgreen)

---

## Sobre o projeto

API REST para processamento de linguagem natural (NLP) construída com FastAPI e modelos pré-treinados do HuggingFace. O projeto segue um roadmap de 4 fases, evoluindo de um esqueleto básico até um pipeline completo com RAG, orquestração e deploy em produção.

---

## Roadmap

| Fase | Período | Descrição | Status |
|------|---------|-----------|--------|
| 1 | Semanas 1–2 | Setup, FastAPI, Docker, primeiro modelo HF | ✅ Concluída |
| 2 | Semanas 3–4 | Pipeline NLP completo, RAG com ChromaDB, PostgreSQL | 🔄 Em andamento |
| 3 | Semanas 5–6 | Orquestração n8n, Redis, Slack/Telegram | ⏳ Pendente |
| 4 | Semanas 7–8 | MLOps, CI/CD, Prometheus, deploy Railway/Fly.io | ⏳ Pendente |

---

## Fase 1 — Setup e base

### O que foi construído

- Estrutura de projeto profissional com separação de responsabilidades
- API REST com FastAPI e documentação Swagger automática
- Containerização completa com Docker e docker-compose
- Integração com modelo HuggingFace de análise de sentimento
- Suite de testes com pytest usando mocks
- Git com conventional commits

### Stack utilizada

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| Python | 3.11 | Linguagem base |
| FastAPI | 0.111 | Framework web |
| Uvicorn | 0.29 | Servidor ASGI |
| HuggingFace Transformers | 4.41 | Modelos de NLP |
| PyTorch | 2.3 | Backend dos modelos |
| Pydantic | 2.7 | Validação de dados |
| Docker | — | Containerização |
| pytest | 9.1 | Testes automatizados |

### Modelo integrado

**cardiffnlp/twitter-roberta-base-sentiment-latest**
- Tarefa: classificação de sentimento
- Labels: `positive`, `neutral`, `negative`
- Score: probabilidade de 0 a 1

### Estrutura de pastas

```
nlp-portfolio/
├── app/
│   ├── main.py              # Entrypoint da aplicação
│   ├── config.py            # Configurações via .env
│   ├── routers/
│   │   ├── health.py        # Endpoint de health check
│   │   └── nlp.py           # Endpoints de NLP
│   ├── models/
│   │   └── hf_loader.py     # Carregamento dos modelos HF
│   ├── schemas/
│   │   ├── requests.py      # Modelos de entrada
│   │   └── responses.py     # Modelos de saída
│   └── tests/
│       └── test_api.py      # Testes automatizados
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── .env.example
```

### Endpoints disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Informações da API |
| GET | `/health/` | Health check |
| POST | `/nlp/sentiment` | Análise de sentimento |
| GET | `/docs` | Documentação Swagger |

### Exemplo de uso

**Request:**
```bash
curl -X POST http://localhost:8000/nlp/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

**Response:**
```json
{
  "text": "I love this product!",
  "label": "positive",
  "score": 0.9823
}
```

### Testes

```bash
# Rodar os testes dentro do container
docker compose exec api pytest app/tests/ -v
```

Resultado da Fase 1:
```
6 passed in 3.54s
```

---

## Como rodar localmente

### Pré-requisitos

- Docker
- Docker Compose

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/nlp-portfolio.git
cd nlp-portfolio

# 2. Copie o arquivo de variáveis de ambiente
cp .env.example .env

# 3. Suba os containers
docker compose up --build

# 4. Acesse a documentação
# http://localhost:8000/docs
```

---

## Variáveis de ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `APP_ENV` | `development` | Ambiente da aplicação |
| `APP_VERSION` | `0.1.0` | Versão da API |
| `HF_CACHE_DIR` | `./models` | Diretório de cache dos modelos |
| `HF_MODEL_SENTIMENT` | `cardiffnlp/twitter-roberta-base-sentiment-latest` | Modelo de sentimento |

---

## Licença

MIT