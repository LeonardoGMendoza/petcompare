# Usa uma imagem oficial do Python, versão leve
FROM python:3.10-slim

# Instala dependências do sistema necessárias para compilar pacotes (como psycopg2) e para o Selenium (Chrome)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wget \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Instalação opcional do Google Chrome para o Selenium (se os robôs forem rodar de dentro do container)
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
#     && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
#     && apt-get update && apt-get install -y google-chrome-stable \
#     && rm -rf /var/lib/apt/lists/*

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia apenas o arquivo de requisitos primeiro (para otimizar o cache do Docker)
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o container
COPY . .

# Expõe a porta que a API vai rodar
EXPOSE 8001

# Comando para iniciar a aplicação
CMD ["python", "run.py"]
