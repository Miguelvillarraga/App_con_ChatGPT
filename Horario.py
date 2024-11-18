import streamlit as st
import pandas as pd

# Configuración inicial
st.title("Gestor de Horarios")

# Autor
st.write("Esta app fue elaborada por **Miguel Angel Villarraga Franco**.")
st.write("Crea materias con horarios para varios días y visualízalos en un horario semanal.")

# Inicialización de datos
if "materias" not in st.session_state:
    st.session_state["materias"] = pd.DataFrame(columns=["Materia", "Día", "Hora Inicio", "Hora Fin"])

# Función para agregar horarios
def agregar_horarios(materia, dias_seleccionados, horarios):
    for dia, horario in zip(dias_seleccionados, horarios):
        nueva_materia = {
            "Materia": materia,
            "Día": dia,
            "Hora Inicio": horario[0],
            "Hora Fin": horario[1]
        }
        st.session_state["materias"] = pd.concat(
            [st.session_state["materias"], pd.DataFrame([nueva_materia])], ignore_index=True
        )

# Entrada de datos
st.header("Agregar Materia y Horarios")
materia = st.text_input("Nombre de la materia")
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
dias_seleccionados = st.multiselect("Selecciona los días", dias)

horarios = []
if dias_seleccionados:
    for dia in dias_seleccionados:
        st.write(f"Horario para {dia}:")
        hora_inicio = st.time_input(f"Hora de inicio ({dia})", key=f"inicio_{dia}")
        hora_fin = st.time_input(f"Hora de fin ({dia})", key=f"fin_{dia}")
        if hora_inicio < hora_fin:
            horarios.append((hora_inicio, hora_fin))
        else:
            st.error(f"El horario para {dia} tiene un error: la hora de inicio debe ser menor que la hora de fin.")

if st.button("Agregar Materia"):
    if materia and dias_seleccionados and len(horarios) == len(dias_seleccionados):
        agregar_horarios(materia, dias_seleccionados, horarios)
        st.success("Materia y horarios agregados correctamente.")
    else:
        st.error("Por favor, verifica que has completado todos los campos y que los horarios son válidos.")

# Visualización de las materias registradas
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
        
        rango_horas = pd.date_range(
            f"2023-01-01 {inicio}", f"2023-01-01 {fin}", freq="30min", inclusive="left"
        ).strftime("%H:%M")

        for hora in rango_horas:
            if hora in horario.index:
                horario.at[hora, row["Día"]] = row["Materia"]

    # Mostrar el horario
    st.table(horario)
else:
    st.write("No hay materias registradas para mostrar el horario.")
