import streamlit as st
import pandas as pd

# Función para calcular el PAPA global
def calcular_papa_global(data):
    data['Ponderado'] = data['Calificación'] * data['Créditos']
    suma_ponderada = data['Ponderado'].sum()
    suma_creditos = data['Créditos'].sum()
    papa_global = suma_ponderada / suma_creditos
    return papa_global

# Función para calcular el PAPA por tipología
def calcular_papa_por_tipologia(data, tipologia):
    data_tipologia = data[data['Tipología'] == tipologia]
    return calcular_papa_global(data_tipologia)

# Interfaz de usuario en Streamlit
st.title("Cálculo del PAPA (UNAL) desde CSV")
st.write("Esta app fue elaborada por **Miguel Angel Villarraga Franco")
st.write("Calcula el PAPA global y por tipología de asignatura a partir de un archivo CSV.")

# Cargar archivo CSV
archivo = st.file_uploader("Cargar archivo CSV", type=["csv"])

if archivo is not None:
    try:
        # Leer el archivo CSV
        data = pd.read_csv(archivo)

        # Verificar si las columnas necesarias existen
        if not all(col in data.columns for col in ['Materia', 'Calificación', 'Créditos', 'Tipología']):
            st.error("El archivo CSV debe contener las columnas: 'Materia', 'Calificación', 'Créditos', 'Tipología'.")
        else:
            # Mostrar los datos cargados
            st.write("Datos cargados desde el archivo CSV:")
            st.dataframe(data)

            # Calcular el PAPA global
            papa_global = calcular_papa_global(data)
            st.subheader(f"PAPA Global: {papa_global:.2f}")

            # Calcular el PAPA por tipología
            tipologias = data['Tipología'].unique()
            seleccion_tipologia = st.selectbox("Selecciona la tipología de asignatura para calcular el PAPA:", tipologias)

            papa_por_tipologia = calcular_papa_por_tipologia(data, seleccion_tipologia)
            st.subheader(f"PAPA por tipología '{seleccion_tipologia}': {papa_por_tipologia:.2f}")

    except Exception as e:
        st.error(f"Error al procesar el archivo CSV: {e}")
else:
    st.write("Por favor, carga un archivo CSV.")
