import streamlit as st
import pandas as pd

# Función para crear las horas posibles (6:00 a 22:00, solo en horas en punto)
def generar_horario():
    horas = [f"{h}:00" for h in range(6, 23)]  # Genera horas de 6:00 a 22:00
    return horas

# Función para agregar clases al horario
def agregar_clase(horario, materia, dias, hora_inicio, duracion):
    # Convertir la hora de inicio y la duración en horas a un rango de horas
    horas_disponibles = generar_horario()
    hora_inicio_idx = horas_disponibles.index(hora_inicio)
    
    # Calcular las horas de clase
    horas_clase = [horas_disponibles[(hora_inicio_idx + i) % len(horas_disponibles)] for i in range(duracion)]
    
    # Agregar la clase a los días seleccionados
    for dia in dias:
        for hora in horas_clase:
            if hora not in horario[dia]:
                horario[dia].append(hora)
    return horario

# Interfaz de usuario en Streamlit
st.title("Gestor de Horarios de Clases")
# Autor
st.write("Esta app fue elaborada por **Miguel Angel Villarraga Franco**.")
st.write("Agrega tus clases al horario seleccionando los días, la hora de inicio y la duración de la clase.")

# Crear las horas posibles
horario = {dia: [] for dia in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']}
horas_disponibles = generar_horario()

# Selección de materia y días
materia = st.text_input("Nombre de la materia:")

# Selección de días múltiples
dias_seleccionados = st.multiselect("Selecciona los días de la semana:", ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'])

# Selección de la hora de inicio
hora_inicio = st.selectbox("Selecciona la hora de inicio:", horas_disponibles)

# Selección de la duración de la clase (de 1 a 3 horas)
duracion = st.slider("Selecciona la duración de la clase (en horas):", 1, 3, 2)

# Agregar la clase al horario
if st.button("Agregar clase"):
    if materia and dias_seleccionados:
        horario = agregar_clase(horario, materia, dias_seleccionados, hora_inicio, duracion)
        st.success(f"Clase '{materia}' agregada en {', '.join(dias_seleccionados)} desde {hora_inicio} durante {duracion} horas.")
    else:
        st.error("Por favor ingresa el nombre de la materia y selecciona al menos un día.")

# Mostrar el horario en una tabla
st.subheader("Horario semanal:")
# Crear un DataFrame con el horario de clases
horario_data = {dia: [''] * 17 for dia in horario}  # Se asume que hay 17 horas en el horario (6:00 a 22:00)
for dia, horas in horario.items():
    for i, hora in enumerate(horas):
        hora_idx = horas_disponibles.index(hora)
        horario_data[dia][hora_idx] = materia  # Asignar la materia en el horario

# Convertir a DataFrame para mostrarlo como tabla
df_horario = pd.DataFrame(horario_data, index=horas_disponibles)
st.table(df_horario)


