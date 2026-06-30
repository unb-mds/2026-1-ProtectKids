FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && python -c "import spacy; spacy.load('pt_core_news_sm'); print('Modelo pt_core_news_sm carregado com sucesso')" \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}