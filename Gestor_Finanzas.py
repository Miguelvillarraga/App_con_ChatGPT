import streamlit as st
import pandas as pd
import datetime as dt

# Configuración inicial
st.title("Gestor de Finanzas Personales")

# Autor
st.write("Esta app fue elaborada por **Miguel Angel Villarraga Franco**.")

# Introducción
st.write("Administra tus ingresos, gastos y metas de ahorro, y genera reportes semanales y mensuales.")

# Simulación de una base de datos local
if "finanzas" not in st.session_state:
    st.session_state["finanzas"] = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Monto", "Comentario"])

# Función para agregar un registro
def agregar_registro(fecha, tipo, categoria, monto, comentario):
    nuevo_registro = {"Fecha": fecha, "Tipo": tipo, "Categoría": categoria, "Monto": monto, "Comentario": comentario}
    st.session_state["finanzas"] = pd.concat(
        [st.session_state["finanzas"], pd.DataFrame([nuevo_registro])], ignore_index=True
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

# Análisis de datos
st.header("Reportes")
modo_reporte = st.selectbox("Selecciona el período del reporte:", ["Semanal", "Mensual"])
fecha_inicio = st.date_input("Fecha de inicio", dt.date.today() - dt.timedelta(days=7))
fecha_fin = st.date_input("Fecha de fin", dt.date.today())

# Filtrar datos
filtro_datos = st.session_state["finanzas"][
    (st.session_state["finanzas"]["Fecha"] >= fecha_inicio) &
    (st.session_state["finanzas"]["Fecha"] <= fecha_fin)
]

if filtro_datos.empty:
    st.write("No hay registros en el rango seleccionado.")
else:
    total_ingresos = filtro_datos[filtro_datos["Tipo"] == "Ingreso"]["Monto"].sum()
    total_gastos = filtro_datos[filtro_datos["Tipo"] == "Gasto"]["Monto"].sum()
    balance = total_ingresos - total_gastos

    st.subheader("Resumen del período")
    st.write(f"**Total de ingresos:** ${total_ingresos:.2f}")
    st.write(f"**Total de gastos:** ${total_gastos:.2f}")
    st.write(f"**Balance neto:** ${balance:.2f}")

    st.subheader("Detalle por categoría")
    detalle_categoria = (
        filtro_datos.groupby(["Tipo", "Categoría"])["Monto"]
        .sum()
        .reset_index()
        .pivot(index="Categoría", columns="Tipo", values="Monto")
        .fillna(0)
    )
    st.dataframe(detalle_categoria)

# Metas de ahorro
st.header("Metas de Ahorro")
if "meta_ahorro" not in st.session_state:
    st.session_state["meta_ahorro"] = {"Monto objetivo": 0, "Progreso": 0}

meta_objetivo = st.number_input("Establece tu meta de ahorro:", min_value=0.0, value=st.session_state["meta_ahorro"]["Monto objetivo"])
ahorro_actual = filtro_datos[(filtro_datos["Tipo"] == "Ingreso") & (filtro_datos["Categoría"] == "Ahorro")]["Monto"].sum()

if st.button("Guardar meta de ahorro"):
    st.session_state["meta_ahorro"]["Monto objetivo"] = meta_objetivo
    st.success("Meta de ahorro actualizada.")

st.write(f"**Progreso actual:** ${ahorro_actual:.2f} / ${meta_objetivo:.2f}")

# Barra de progreso
if meta_objetivo > 0:
    progreso = min(ahorro_actual / meta_objetivo, 1.0)
    st.progress(progreso)
