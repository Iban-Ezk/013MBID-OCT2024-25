import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#Lectura de datos
df = pd.read_csv("../../../data/final/datos_finales.csv", sep=";")

# Configuración de la página
st.set_page_config(
    page_title="Herramienta de Visualización de Datos - 13MBID",
    layout="wide",
)

# Titulo de la aplicación
st.title("Herramienta de Visualización de Datos - 13MBID")
st.write(
    "Esta aplicación permite explorar y visualizar los datos del proyecto en curso."
)
st.write("Desarrollado por: Ivan Ezcurdia Razquin")
st.markdown('----')

# Gráficos
st.header("Gráficos")
st.subheader("Caracterización de los créditos otorgados:")

# Cantidad de créditos por objetivo del mismo

creditos_x_objetivo = px.histogram(df, x='objetivo_credito', 
                                   title='Conteo de créditos por objetivo')
creditos_x_objetivo.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')

# Visualización
st.plotly_chart(creditos_x_objetivo, use_container_width=True)

# Histograma de los importes de créditos otorgados

histograma_importes = px.histogram(df, x='importe_solicitado', nbins=10, title='Importes solicitados en créditos')
histograma_importes.update_layout(xaxis_title='Importe solicitado', yaxis_title='Cantidad')

st.plotly_chart(histograma_importes, use_container_width=True)

# Conteo de ocurrencias por estado
estado_credito_counts = df['estado_credito_N'].value_counts()

# Gráfico de tarta de estos valores
fig = go.Figure(data=[go.Pie(labels=estado_credito_counts.index, values=estado_credito_counts)])
fig.update_layout(title_text='Distribución de créditos por estado registrado')

st.plotly_chart(fig, use_container_width=True)

tipo_credito = st.multiselect(
    "Selecciona el/los objetivo(s) del crédito",
    df['objetivo_credito'].unique(),
    default=[]
)

st.write("Tipo(s) de crédito seleccionado(s):", tipo_credito)

# Filtrar solo si hay selecciones
if tipo_credito:
    df_filtrado = df[df['objetivo_credito'].isin(tipo_credito)]
else:
    # Si no hay selección, puedes mostrar el DataFrame completo o vaciar el gráfico
    df_filtrado = df

col1, col2 = st.columns(2)
with col1:
# Continuar con el gráfico
    barras_apiladas = px.histogram(df_filtrado, x='objetivo_credito', color='estado_credito_N',
                            title='Distribución de créditos por estado y objetivo',
                            barmode='stack'
)
    barras_apiladas.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')
    st.plotly_chart(barras_apiladas, use_container_width=True)

with col2:
# Conteo de ocurrencias por caso
    falta_pago_counts = df_filtrado['falta_pago'].value_counts()
    # Create a Pie chart
    fig = go.Figure(data=[go.Pie(labels=falta_pago_counts.index, values=falta_pago_counts)])
    fig.update_layout(title_text='Distribución de créditos en función de registro de mora')
    st.plotly_chart(fig, use_container_width=True)

# Definir el orden personalizado
orden_antiguedad = ['menor_2y', '2y_a_4y', 'mayor_4y']

# Ordenar los datos según el orden personalizado
df_ordenado = df.groupby('antiguedad_cliente')['importe_solicitado'].mean().reset_index()
df_ordenado['antiguedad_cliente'] = pd.Categorical(df_ordenado['antiguedad_cliente'], categories=orden_antiguedad, ordered=True)
df_ordenado = df_ordenado.sort_values('antiguedad_cliente')

# Crear el gráfico de líneas
lineas_importes_antiguedad = px.line(df_ordenado, x='antiguedad_cliente', y='importe_solicitado',
                                     title='Evolución de los importes solicitados por antigüedad del cliente')
lineas_importes_antiguedad.update_layout(xaxis_title='Antigüedad del cliente', yaxis_title='Importe solicitado promedio')

st.plotly_chart(lineas_importes_antiguedad, use_container_width=True)

# Distribución de los importes solicitados (`importe_solicitado`) por objetivo del crédito (`objetivo_credito`) en un gráfico de cajas
cajas_grafico = px.box(df, x='objetivo_credito', y='importe_solicitado',
              title='Distribución de importes solicitados por objetivo del crédito',
              labels={'objetivo_credito': 'Objetivo del crédito', 'importe_solicitado': 'Importe solicitado'})

st.plotly_chart(cajas_grafico, use_container_width=True)

# Relación entre el importe solicitado (`importe_solicitado`) con la duración del crédito (`duracion_credito`), coloreado por estado del crédito (`estado_credito_N`) en un gráfico de dispersión.
dispersion_grafico = px.scatter(df, x='duracion_credito', y='importe_solicitado',
                  color='estado_credito_N',
                  title='Relación entre importe solicitado y duración del crédito',
                  labels={'duracion_credito': 'Duración del crédito', 'importe_solicitado': 'Importe solicitado', 'estado_credito_N': 'Estado del crédito'})

st.plotly_chart(dispersion_grafico, use_container_width=True)

# Análisis de la correlación entre variables como `importe_solicitado`, `duracion_credito`, y `personas_a_cargo` en un mapa de calor.
import plotly.figure_factory as ff

# Selecciona las variables numéricas para la correlación
variables = ['importe_solicitado', 'duracion_credito', 'personas_a_cargo']
corr_matrix = df[variables].corr()

# Crear el mapa de calor
mapa_calor = ff.create_annotated_heatmap(
    z=corr_matrix.values,
    x=variables,
    y=variables,
    annotation_text=corr_matrix.round(2).values,
    colorscale='Viridis'
)

mapa_calor.update_layout(title='Mapa de calor de correlaciones entre variables')

st.plotly_chart(mapa_calor, use_container_width=True)


