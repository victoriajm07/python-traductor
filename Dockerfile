FROM continuumio/anaconda3

# Actualiza los paquetes del sistema y limpia los archivos temporales
RUN apt-get update && \
    apt-get install -y libgtk2.0-dev && \
    rm -rf /var/lib/apt/lists/*

# Actualiza Conda y asegúrate de usar una versión existente de Python
RUN /opt/conda/bin/conda update --yes -n base -c defaults conda && \
    /opt/conda/bin/conda install --yes python=3.10

WORKDIR /traductor

# Copia todo el contenido del directorio actual al contenedor
COPY . /traductor

# Instala las dependencias de Python usando pip
RUN /opt/conda/bin/pip install -r requirements.txt

# Expone el puerto que Streamlit utiliza por defecto
EXPOSE 8501

# Configura un comando para ejecutar Streamlit al iniciar el contenedor
CMD ["streamlit", "run", "src/traductor.py", "--server.port=8501", "--server.address=0.0.0.0"]