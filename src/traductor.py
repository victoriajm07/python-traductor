# Instalar antes  translate y PyPDF2

# pip install mtranslate
# pip install PyPDF2

# Para descargar el entorno web / vista 
# pip install streamlit

import PyPDF2
from mtranslate import translate
import streamlit as st
from io import BytesIO
import requests

url = "https://es.libretranslate.com/languages"

respuesta = requests.get(url)
if respuesta.status_code == 200:
    datos_json = respuesta.json()
    lista_idiomas = {idioma["code"]: idioma["name"] for idioma in datos_json}
    lista_idiomas['gl'] = "Gallego"
else:
    st.error("No se pudo obtener la lista de idiomas")
    lista_idiomas = {}

def traducir_pdf(file, idioma_origen, idioma_destino):

    traduccion = []
    pdf_bytes = file.getvalue()
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
    num_paginas = len(pdf_reader.pages)

        # Traducir el texto de cada página por separado
    texto_traducido = []
    for pagina_num in range(num_paginas):
        pagina = pdf_reader.pages[pagina_num]
        texto_pagina = pagina.extract_text()
            # Dividir el texto en partes más pequeñas (aquí, límite de 5000 caracteres)
        partes_texto = [texto_pagina[i:i+5000] for i in range(0, len(texto_pagina), 5000)]

            # Traducir cada parte del texto
        partes_traducidas = []
        for parte in partes_texto:
            traduccion = translate(parte, to_language=idioma_destino, from_language=idioma_origen)
            partes_traducidas.append(traduccion)

            # Concatenar las partes traducidas en una sola cadena
        texto_traducido_pagina = ' '.join(partes_traducidas)
        texto_traducido.append(texto_traducido_pagina)
    return '/n/n'.join(texto_traducido)

st.title('Aplicación para Traducir Documentos PDF')

uploaded_file = st.file_uploader("Selecciona el PDF a traducir", type="pdf")

col1, col2 = st.columns(2)

with col1:
    idioma_origen = st.selectbox("Origen ", list(lista_idiomas.keys()), format_func=lambda x: lista_idiomas[x])

with col2:
    idioma_destino = st.selectbox("Destino ", list(lista_idiomas.keys()), format_func=lambda x: lista_idiomas[x])

if uploaded_file is not None:
    if st.button('Traducir PDF'):
        texto_traducido = traducir_pdf(uploaded_file, idioma_origen, idioma_destino)
        st.text_area("Texto Traducido", value=texto_traducido, height=300)
        
        # Permitir al usuario descargar el texto traducido
        result_file = BytesIO()
        result_file.write(texto_traducido.encode('utf-8'))
        result_file.seek(0)
        st.download_button(label="Descargar texto traducido",
                           data=result_file,
                           file_name="texto_traducido.txt",
                           mime="text/plain")