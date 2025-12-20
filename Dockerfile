cat > Dockerfile << 'EOF'
FROM python:3.10-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copie des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Variables d'environnement par défaut
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Commande par défaut
CMD ["python", "market_collector.py"]
EOF