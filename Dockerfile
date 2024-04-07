FROM python:3.12.2-alpine
LABEL authors="jvega"

# Copia todo el contenido actual del directorio de construcción al directorio de trabajo
COPY . /app

# Establece el directorio de trabajo en /log_save
WORKDIR /app

RUN apk add build-base

# Instala dependencias necesarias para Poetry
RUN pip install poetry

# Instala las dependencias de Poetry
RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "-u", "-m", "apps.api.__main__"]