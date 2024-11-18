import streamlit as st

# Título de la app
st.title("Conversor Universal")

# Autor
st.write("Esta app fue elaborada por **Miguel Angel Villarraga Franco**.")

# Introducción
st.write("Selecciona una categoría y el tipo de conversión que deseas realizar.")

# Diccionario con las conversiones y sus funciones
conversiones = {
    "Temperatura": {
        "Celsius a Fahrenheit": lambda c: (c * 9/5) + 32,
        "Fahrenheit a Celsius": lambda f: (f - 32) * 5/9,
        "Celsius a Kelvin": lambda c: c + 273.15,
        "Kelvin a Celsius": lambda k: k - 273.15,
    },
    "Longitud": {
        "Pies a metros": lambda ft: ft * 0.3048,
        "Metros a pies": lambda m: m / 0.3048,
        "Pulgadas a centímetros": lambda in_: in_ * 2.54,
        "Centímetros a pulgadas": lambda cm: cm / 2.54,
    },
    "Peso/Masa": {
        "Libras a kilogramos": lambda lb: lb * 0.453592,
        "Kilogramos a libras": lambda kg: kg / 0.453592,
        "Onzas a gramos": lambda oz: oz * 28.3495,
        "Gramos a onzas": lambda g: g / 28.3495,
    },
    "Volumen": {
        "Galones a litros": lambda gal: gal * 3.78541,
        "Litros a galones": lambda l: l / 3.78541,
        "Pulgadas cúbicas a centímetros cúbicos": lambda in3: in3 * 16.3871,
        "Centímetros cúbicos a pulgadas cúbicas": lambda cm3: cm3 / 16.3871,
    },
    "Tiempo": {
        "Horas a minutos": lambda h: h * 60,
        "Minutos a segundos": lambda min_: min_ * 60,
        "Días a horas": lambda d: d * 24,
        "Semanas a días": lambda w: w * 7,
    },
    "Velocidad": {
        "Millas por hora a kilómetros por hora": lambda mph: mph * 1.60934,
        "Kilómetros por hora a metros por segundo": lambda kmh: kmh / 3.6,
        "Nudos a millas por hora": lambda knots: knots * 1.15078,
        "Metros por segundo a pies por segundo": lambda mps: mps * 3.28084,
    },
    "Área": {
        "Metros cuadrados a pies cuadrados": lambda m2: m2 * 10.7639,
        "Pies cuadrados a metros cuadrados": lambda ft2: ft2 / 10.7639,
        "Kilómetros cuadrados a millas cuadradas": lambda km2: km2 / 2.58999,
        "Millas cuadradas a kilómetros cuadrados": lambda mi2: mi2 * 2.58999,
    },
    "Energía": {
        "Julios a calorías": lambda j: j / 4.184,
        "Calorías a kilojulios": lambda cal: cal * 0.004184,
        "Kilovatios-hora a megajulios": lambda kwh: kwh * 3.6,
        "Megajulios a kilovatios-hora": lambda mj: mj / 3.6,
    },
    "Presión": {
        "Pascales a atmósferas": lambda pa: pa / 101325,
        "Atmósferas a pascales": lambda atm: atm * 101325,
        "Barras a libras por pulgada cuadrada": lambda bar: bar * 14.5038,
        "Libras por pulgada cuadrada a bares": lambda psi: psi / 14.5038,
    },
    "Tamaño de datos": {
        "Megabytes a gigabytes": lambda mb: mb / 1024,
        "Gigabytes a Terabytes": lambda gb: gb / 1024,
        "Kilobytes a megabytes": lambda kb: kb / 1024,
        "Terabytes a petabytes": lambda tb: tb / 1024,
    },
}

# Selección de categoría
categoria = st.selectbox("Selecciona una categoría:", list(conversiones.keys()))

# Selección de conversión dentro de la categoría
tipo_conversion = st.selectbox("Selecciona un tipo de conversión:", list(conversiones[categoria].keys()))

# Entrada del valor a convertir
valor = st.number_input("Ingresa el valor a convertir:", min_value=0.0)

# Realizar la conversión
if st.button("Convertir"):
    resultado = conversiones[categoria][tipo_conversion](valor)
    st.success(f"El resultado de convertir {valor} es: {resultado:.2f}")
