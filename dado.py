import streamlit as st
import numpy as np
import pandas as pd
from scipy import stats

# Función para simular el lanzamiento del dado
def lanzar_dado():
    return np.random.randint(1, 7, size=20)  # Lanza el dado 20 veces

# Generar los resultados de los lanzamientos
resultados = lanzar_dado()

# Calcular estadísticas
media = np.mean(resultados)
mediana = np.median(resultados)

# Intentar obtener la moda
moda_resultado = stats.mode(resultados)

# Verificar si hay moda
if moda_resultado.count[0] > 0:
    moda = moda_resultado.mode[0]
else:
    moda = "Sin moda"

varianza = np.var(resultados)
desviacion_estandar = np.std(resultados)

# Crear un DataFrame para las frecuencias
frecuencias = pd.DataFrame({
    'Número': [1, 2, 3, 4, 5, 6],
    'Frecuencia': [np.sum(resultados == i) for i in range(1, 7)]
})

# Mostrar la aplicación en Streamlit
st.title("Simulación de Lanzamiento de un Dado")
st.write("**App desarrollada por Miguel Ángel Villarraga Franco**")

st.write(f"**Resultados de los 20 lanzamientos del dado:**")
st.write(resultados)

st.write(f"**Análisis estadístico:**")
st.write(f"Media: {media}")
st.write(f"Mediana: {mediana}")
st.write(f"Moda: {moda}")
st.write(f"Varianza: {varianza}")
st.write(f"Desviación estándar: {desviacion_estandar}")

st.write("**Tabla de frecuencias de los lanzamientos del dado:**")
st.write(frecuencias)

# Botón para regenerar resultados y estadísticas
if st.button('Lanzar el dado nuevamente'):
    resultados = lanzar_dado()
    st.write(resultados)
