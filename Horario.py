import streamlit as st
import pandas as pd
import numpy as np

# Configuración inicial
st.title("Gestor de Horarios")

# Autor
st.write("Esta app fue elaborada por **Miguel Angel Villarraga Franco**.")

# Introducción
st.write("Crea materias con sus respectivos horarios y visualízalos en un horario semanal.")

# Inicialización de datos
if "materias" not in st.session_state:
    st.session_state["materias"] = pd.DataFrame(columns=["Materia", "Día", "Hora Inicio", "Hora Fin"])

# Función para agregar una materia
def agregar_materia(materia, dia, hora_inicio, hora_fin):
    nueva_materia = {"Materia": materia, "Día": dia, "Hora Inicio": hora_inicio, "Hora Fin": hora_fin}
    st.session_state["materias"] = pd.concat(
        [st.session_state["materias"], pd.DataFrame([nueva_materia])], ignore_index=True
    )

# Entrada de datos
st.header("Agregar Materia")
materia = st.text_input("Nombre de la materia")
dia = st.selectbox("Día de la semana", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"])
hora_inicio = st.time_input("Hora de inicio")
hora_fin = st.time_input("Hora de fin")

if st.button("Agregar"):
    if materia and hora_inicio < hora_fin:
        agregar_materia(materia, dia, hora_inicio, hora_fin)
        st.success("Materia agregada correctamente.")
    else:
        st.error("Por favor, completa todos los campos correctamente y verifica los horarios.")

# Visualización de las materias
st.header("Materias Registradas")
if st.session_state["materias"].empty:
    st.write("No hay materias registradas aún.")
else:
    st.dataframe(st.session_state["materias"])

# Generar horario semanal
st.header("Horario Semanal")

if not st.session_state["materias"].empty:
    # Crear una tabla vacía para el horario
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    horas = pd.date_range("06:00", "22:00", freq="30min").strftime("%H:%M")

    horario = pd.DataFrame("", index=horas, columns=dias)

    # Llenar la tabla con las materias
    for _, row in st.session_state["materias"].iterrows():
        inicio = row["Hora Inicio"].strftime("%H:%M")
        fin = row["Hora Fin"].strftime("%H:%M")
        rango_horas = pd.date_range(inicio, fin, freq="30min", closed="left").strftime("%H:%M")

        for hora in rango_horas:
            if hora in horario.index:
                horario.at[hora, row["Día"]] = row["Materia"]

    # Mostrar el horario
    st.table(horario)
else:
    st.write("No hay materias registradas para mostrar el horario.")
