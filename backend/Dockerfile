FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    curl \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && python -c "import spacy; spacy.load('pt_core_news_sm'); print('Modelo pt_core_news_sm carregado com sucesso')" \
    && apt-get purge -y --auto-remove gcc \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]