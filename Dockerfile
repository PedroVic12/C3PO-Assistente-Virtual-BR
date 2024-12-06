# Usar uma imagem base com Python e Node.js
FROM node:16-buster as build

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do backend e frontend
COPY . .

# Instalar dependências do Python
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt

# Instalar dependências do Node.js
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Expor as portas
EXPOSE 7777
EXPOSE 8888

# Comando para iniciar o Flask e o React
CMD ["bash", "-c", "pm2 start app.py --name c3po-backend && pm2 start npm --name c3po-frontend -- run dev"]