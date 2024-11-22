# Etapa base
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copie o código fonte para o container
COPY src /app/src
COPY data /app/data

# Copie o arquivo requirements.txt para o container e instale as dependências
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Porta exposta
EXPOSE 8501

# Comando para rodar o app
CMD ["streamlit", "run", "src/frontend/pages/app.py", "--server.port=8501", "--server.address=0.0.0.0"]


