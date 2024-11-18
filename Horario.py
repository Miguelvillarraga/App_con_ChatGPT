import streamlit as st
import pandas as pd

# Función para crear el horario
def generar_horario():
    # Definir las horas disponibles (de 6:00 a 22:00, solo en horas en punto)
    horas = [f"{h}:00" for h in range(6, 23)]
    return horas

# Función para agregar clases al horario
def agregar_clase(horario, materia, dia, hora_inicio, duracion):
    # Convertir la hora de inicio y la duración en horas a un rango de horas
    hora_inicio_idx = horario.index(hora_inicio)
    horas_clase = [horario[(hora_inicio_idx + i) % len(horario)] for i in range(duracion)]
    
    # Agregar la clase al horario
    for hora in horas_clase:
        if hora not in horario[dia]:
            horario[dia].append(hora)
    return horario

# Autor
st.write("Esta app fue elaborada por **Miguel Angel Villarraga Franco**.")
# Interfaz de usuario en Streamlit
st.title("Gestor de Horarios de Clases")
st.write("Agrega tus clases al horario seleccionando el día, la hora de inicio y la duración.")

# Crear las horas posibles
horario = {dia: [] for dia in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']}
horas_disponibles = generar_horario()

# Selección de materia y días
materia = st.text_input("Nombre de la materia:")
dia_seleccionado = st.selectbox("Selecciona el día de la semana:", ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'])

# Selección de la hora de inicio (debe ser en horas en punto)
hora_inicio = st.selectbox("Selecciona la hora de inicio:", horas_disponibles)

# Duración de la clase (mínimo 2 horas)
duracion = st.slider("Duración de la clase (en horas):", min_value=2, max_value=4, value=2)

# Agregar la clase al horario
if st.button("Agregar clase"):
    if materia:
        horario = agregar_clase(horario, materia, dia_seleccionado, hora_inicio, duracion)
        st.success(f"Clase '{materia}' agregada al {dia_seleccionado} desde {hora_inicio} durante {duracion} horas.")
    else:
        st.error("Por favor ingresa el nombre de la materia.")

# Mostrar el horario
st.subheader("Horario semanal:")
for dia, horas in horario.items():
    if horas:
        st.write(f"{dia}: {', '.join(horas)}")
    else:
        st.write(f"{dia}: No hay clases programadas.")
