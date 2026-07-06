import streamlit as st
import pandas as pd

# 1. Configuración visual de la página
st.set_page_config(page_title="Portal de Notas", page_icon="🎓", layout="centered")
st.title("Portal de Notas - Historial Académico Completo")

# 2. Conexión en vivo con Google Sheets
# REEMPLAZÁ el link de abajo por tu link de Drive terminado en /export?format=csv
LINK_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/1YwVWkrLj35kJpGvFkxfkX7xPlYoL0tDL/export?format=csv"

def cargar_datos():
    # Descarga y lee la planilla de Drive en tiempo real
    return pd.read_csv(LINK_GOOGLE_SHEETS)

try:
    df = cargar_datos()
except Exception as e:
    st.error("🚨 Hubo un problema al conectar con la planilla de Google Drive. Verificá el enlace.")
    st.stop()

# Convertimos el DNI a texto y limpiamos espacios para evitar errores de tipeo
df['DNI'] = df['DNI'].astype(str).str.strip()

# 3. Interfaz de usuario
st.write("Ingresá tu DNI para consultar tus calificaciones de cada instancia, las devoluciones y tu promedio final.")

dni_ingresado = st.text_input("Tu DNI (sin puntos ni espacios):")

if dni_ingresado:
    # Buscamos la fila que coincida exactamente con el DNI ingresado
    alumno = df[df['DNI'] == dni_ingresado.strip()]

    if not alumno.empty:
        st.success("¡Datos encontrados!")
        
        # Extraemos los datos principales
        nombre_completo = f"{alumno['Nombre'].iloc[0]} {alumno['Apellido'].iloc[0]}"
        
        st.subheader(f"Alumno/a: {nombre_completo}")
        st.divider()

        # --- SECCIÓN DE NOTAS (Métricas distribuidas) ---
        st.markdown("### 📊 Calificaciones")
        
        # Primera fila de notas: Procesos y parciales
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Autoevaluación", value=alumno['Autoevaluación_Nota'].iloc[0])
        with col2:
            st.metric(label="Primer Parcial", value=alumno['Parcial1_Nota'].iloc[0])
        with col3:
            st.metric(label="Segundo Parcial", value=alumno['Parcial2_Nota'].iloc[0])
        
        # Segunda fila de notas: Instancia Final y Promedio destacado
        st.write("") # Espacio estético
        col4, col5 = st.columns(2)
        with col4:
            st.metric(label="Examen Final", value=alumno['Final_Nota'].iloc[0])
        with col5:
            st.metric(label="Promedio Final", value=alumno['Promedio'].iloc[0])
        
        st.divider()

        # --- SECCIÓN DE FEEDBACKS (Menús desplegables ordenados) ---
        st.markdown("### 💬 Devoluciones de la Profesora")
        
        # Función auxiliar para controlar celdas vacías en los comentarios
        def obtener_comentario(columna):
            texto = alumno[columna].iloc[0]
            return texto if pd.notna(texto) and str(texto).strip() != "" else "Sin comentarios registrados para esta instancia."

        with st.expander("📬 Feedback: Autoevaluación", expanded=False):
            st.write(obtener_comentario('Autoevaluación_Feedback'))
            
        with st.expander("📝 Feedback: Primer Parcial", expanded=False):
            st.write(obtener_comentario('Parcial1_Feedback'))
            
        with st.expander("💻 Feedback: Segundo Parcial", expanded=False):
            st.write(obtener_comentario('Parcial2_Feedback'))
            
        with st.expander("🏆 Feedback: Instancia Final", expanded=False):
            st.write(obtener_comentario('Final_Feedback'))

    else:
        st.warning("No encontramos registros con ese DNI. Por favor, revisá el número o consultá con la profesora.")
