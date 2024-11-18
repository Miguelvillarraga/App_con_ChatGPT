import streamlit as st
import pandas as pd

# Configuración inicial
st.title("Calculadora de PAPA - UNAL")
st.write("Esta app fue elaborada por **Miguel Angel Villarraga Franco**.")
st.write("Calcula tu PAPA global y por tipología de asignatura.")

# Inicialización de datos
if "materias" not in st.session_state:
    st.session_state["materias"] = pd.DataFrame(columns=["Asignatura", "Tipología", "Créditos", "Nota"])

# Función para agregar una materia
def agregar_materia(asignatura, tipologia, creditos, nota):
    nueva_materia = {
        "Asignatura": asignatura,
        "Tipología": tipologia,
        "Créditos": creditos,
        "Nota": nota
    }
    st.session_state["materias"] = pd.concat(
        [st.session_state["materias"], pd.DataFrame([nueva_materia])], ignore_index=True
    )

# Entrada de datos
st.header("Agregar Materias")
asignatura = st.text_input("Nombre de la asignatura")
tipologia = st.selectbox("Tipología de la asignatura", [
    "Fundamentación obligatoria", 
    "Fundamentación optativa", 
    "Disciplinar obligatoria", 
    "Disciplinar optativa", 
    "Trabajo de grado", 
    "Nivelación", 
    "Libre elección"
])
creditos = st.number_input("Créditos de la asignatura", min_value=1, step=1)
nota = st.number_input("Nota obtenida (entre 0.0 y 5.0)", min_value=0.0, max_value=5.0, step=0.1)

if st.button("Agregar"):
    if asignatura and creditos > 0 and 0 <= nota <= 5:
        agregar_materia(asignatura, tipologia, creditos, nota)
        st.success("Asignatura agregada correctamente.")
    else:
        st.error("Por favor, completa todos los campos correctamente.")

# Visualización de las materias
st.header("Materias Registradas")
if st.session_state["materias"].empty:
    st.write("No hay materias registradas aún.")
else:
    st.dataframe(st.session_state["materias"])

# Cálculo del PAPA
st.header("Cálculo del PAPA")

if not st.session_state["materias"].empty:
    # PAPA global
    total_creditos = st.session_state["materias"]["Créditos"].sum()
    suma_ponderada = (st.session_state["materias"]["Créditos"] * st.session_state["materias"]["Nota"]).sum()
    papa_global = suma_ponderada / total_creditos if total_creditos > 0 else 0

    st.subheader("PAPA Global")
    st.write(f"**PAPA:** {papa_global:.2f}")

    # PAPA por tipología
    st.subheader("PAPA por Tipología")
    tipologias = st.session_state["materias"]["Tipología"].unique()

    for tipo in tipologias:
        materias_tipo = st.session_state["materias"][st.session_state["materias"]["Tipología"] == tipo]
        total_creditos_tipo = materias_tipo["Créditos"].sum()
        suma_ponderada_tipo = (materias_tipo["Créditos"] * materias_tipo["Nota"]).sum()
        papa_tipo = suma_ponderada_tipo / total_creditos_tipo if total_creditos_tipo > 0 else 0
        st.write(f"- **{tipo}:** {papa_tipo:.2f}")
