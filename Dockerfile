# Use uma imagem base do Python
FROM python:3.12 as backend

# Defina o diretório de trabalho para o backend
WORKDIR /app

# Copie os arquivos de requisitos e instale as dependências do backend
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copie o restante dos arquivos do projeto
COPY . .

# Exponha a porta que seu aplicativo Flask está usando
EXPOSE 7777

# Use uma imagem base do Node.js para o frontend
FROM node:18 as frontend

# Defina o diretório de trabalho para o frontend
WORKDIR /app/frontend

# Copie os arquivos do frontend e instale as dependências
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Copie o restante dos arquivos do frontend
COPY frontend/ .

# Exponha a porta que seu aplicativo React está usando
EXPOSE 8080

# Comando para rodar o aplicativo Flask
CMD ["python", "app.py"]