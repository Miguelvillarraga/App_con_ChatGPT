import streamlit as st
import pandas as pd
import datetime as dt

# Configuración inicial
st.title("Gestor de Finanzas Personales")
st.write("Administra tus ingresos, gastos y metas de ahorro, y genera reportes semanales y mensuales.")

# Simulación de una base de datos local
if "finanzas" not in st.session_state:
    st.session_state["finanzas"] = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Monto", "Comentario"])

if "metas" not in st.session_state:
    st.session_state["metas"] = pd.DataFrame(columns=["Nombre", "Monto objetivo", "Progreso", "Fecha límite"])

# Función para agregar un registro
def agregar_registro(fecha, tipo, categoria, monto, comentario):
    nuevo_registro = {"Fecha": fecha, "Tipo": tipo, "Categoría": categoria, "Monto": monto, "Comentario": comentario}
    st.session_state["finanzas"] = pd.concat(
        [st.session_state["finanzas"], pd.DataFrame([nuevo_registro])], ignore_index=True
    )

# Función para agregar una meta
def agregar_meta(nombre, monto_objetivo, fecha_limite):
    nueva_meta = {"Nombre": nombre, "Monto objetivo": monto_objetivo, "Progreso": 0.0, "Fecha límite": fecha_limite}
    st.session_state["metas"] = pd.concat(
        [st.session_state["metas"], pd.DataFrame([nueva_meta])], ignore_index=True
    )

# Entrada de datos
st.header("Agregar Registro")
fecha = st.date_input("Fecha", dt.date.today())
tipo = st.selectbox("Tipo de movimiento", ["Ingreso", "Gasto"])
categoria = st.selectbox("Categoría", ["Salario", "Alquiler", "Comida", "Transporte", "Ahorro", "Ocio", "Otros"])
monto = st.number_input("Monto", min_value=0.0, format="%.2f")
comentario = st.text_area("Comentario (opcional)")

if st.button("Agregar"):
    agregar_registro(fecha, tipo, categoria, monto, comentario)
    st.success("Registro agregado correctamente.")

# Visualización de registros
st.header("Historial de Finanzas")
if st.session_state["finanzas"].empty:
    st.write("No hay registros aún.")
else:
    st.dataframe(st.session_state["finanzas"])

# Gestión de metas de ahorro
st.header("Gestión de Metas de Ahorro")

# Crear una nueva meta
st.subheader("Crear Meta")
nombre_meta = st.text_input("Nombre de la meta")
monto_meta = st.number_input("Monto objetivo", min_value=0.0, format="%.2f")
fecha_limite_meta = st.date_input("Fecha límite")

if st.button("Guardar Meta"):
    if nombre_meta and monto_meta > 0:
        agregar_meta(nombre_meta, monto_meta, fecha_limite_meta)
        st.success(f"Meta '{nombre_meta}' creada correctamente.")
    else:
        st.error("Por favor, completa todos los campos.")

# Visualizar y actualizar metas
st.subheader("Metas Actuales")
if st.session_state["metas"].empty:
    st.write("No hay metas creadas aún.")
else:
    for index, meta in st.session_state["metas"].iterrows():
        st.write(f"**Meta:** {meta['Nombre']}")
        st.write(f"- Monto objetivo: ${meta['Monto objetivo']:.2f}")
        st.write(f"- Progreso actual: ${meta['Progreso']:.2f}")
        st.write(f"- Fecha límite: {meta['Fecha límite']}")

        # Cálculo de progreso
        ahorro_actual = st.session_state["finanzas"][
            (st.session_state["finanzas"]["Tipo"] == "Ingreso") & 
            (st.session_state["finanzas"]["Categoría"] == "Ahorro")
        ]["Monto"].sum()

        progreso = min(ahorro_actual / meta["Monto objetivo"], 1.0) if meta["Monto objetivo"] > 0 else 0.0

        # Actualizar progreso en la base de datos
        st.session_state["metas"].at[index, "Progreso"] = ahorro_actual

        # Mostrar barra de progreso
        st.progress(progreso)

        st.write("---")
