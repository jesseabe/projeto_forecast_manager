# Forecast Manager

Forecast Manager é uma aplicação desenvolvida com Streamlit para gerenciar e visualizar previsões. Este repositório contém os arquivos necessários para configurar e executar a aplicação em um ambiente Docker.

## 📋 Pré-requisitos

Certifique-se de ter instalado em sua máquina:
- [Docker](https://www.docker.com/get-started)

## 🚀 Como executar a aplicação

Siga os passos abaixo para rodar a aplicação localmente:

### 1️⃣ Clone este repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd projeto_forecast_manager
```

## 2️⃣ Construa a imagem Docker
Execute o comando para criar a imagem Docker:
```bash
docker build -t forecast_manager .
```
## 3️⃣ Rode o container
Inicie o container da aplicação expondo a porta padrão do Streamlit 8501:
```bash
docker run -p 8501:8501 forecast_manager_container forecast_manager
```

## Acesse a aplicação
Abra o navegador e acesse:
```bash
http://localhost:8501
```

