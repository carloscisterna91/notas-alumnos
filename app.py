import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Consulta de Notas", page_icon="🎓")
st.title("Portal de Notas - Autoevaluación")

# 2. Cargar los datos del Excel
def cargar_datos():
    # Lee el archivo Excel que está en la misma carpeta
    return pd.read_excel("notas.xlsx")

try:
    df = cargar_datos()
except FileNotFoundError:
    st.error("🚨 No se encontró el archivo 'notas.xlsx'. Por favor, asegurate de que esté en la misma carpeta.")
    st.stop()

# 3. Interfaz para el alumno
st.write("Ingresá tu nombre y apellido para ver tu calificación y los comentarios de la profesora.")

# Creamos dos columnas para que quede un formulario más prolijo
col1, col2 = st.columns(2)
with col1:
    nombre_ingresado = st.text_input("Tu Nombre:")
with col2:
    apellido_ingresado = st.text_input("Tu Apellido:")

# 4. Lógica de búsqueda
# El programa solo busca si el alumno ya escribió en ambas cajas
if nombre_ingresado and apellido_ingresado:
    
    # Preparamos las columnas ignorando mayúsculas y espacios extra
    nombres_excel = df['Nombre'].astype(str).str.strip().str.lower()
    apellidos_excel = df['Apellido'].astype(str).str.strip().str.lower()
    
    # Filtramos donde coincidan EXACTAMENTE el nombre y el apellido
    alumno = df[(nombres_excel == nombre_ingresado.strip().lower()) & 
                (apellidos_excel == apellido_ingresado.strip().lower())]

    if not alumno.empty:
        st.success("¡Datos encontrados!")
        
        # Extraemos la información de esa fila específica
        nombre_real = alumno['Nombre'].iloc[0]
        apellido_real = alumno['Apellido'].iloc[0]
        nota = alumno['Nota'].iloc[0]
        feedback = alumno['Feedback'].iloc[0]
        
        # Mostramos los resultados en pantalla
        st.subheader(f"Alumno/a: {nombre_real} {apellido_real}")
        st.metric(label="Tu Nota", value=nota)
        st.info(f"**Comentarios:**\n\n{feedback}")
    else:
        st.warning("No encontramos a nadie con ese nombre y apellido. Revisá que estén escritos tal cual aparecen en la lista de la profesora.")