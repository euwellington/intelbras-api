# Use uma imagem base do Python (escolha a versão adequada)
FROM python:3.9

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código-fonte para o diretório de trabalho
COPY . .

# Exponha a porta que o aplicativo Flask estará ouvindo
EXPOSE 5000

# Comando para iniciar o aplicativo Flask
CMD ["python", "app.py"]
