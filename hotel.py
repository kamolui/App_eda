import streamlit as st
import pandas as pd
import numpy as np
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import pydeck

# Web App Title
st.markdown('''
# **Hospedaje EDA App.**
## Esta APP realiza un analisis exploratorio de los datos dados.
---
''')

# Upload CSV data
with st.sidebar.header('1. Carga tus datos tipo CSV.'):
    uploaded_file = st.sidebar.file_uploader("Carga tu archivo CSV de entrada. ", type=["csv"])
    st.sidebar.markdown("""
[Archivo CSV de muestra ](https://raw.githubusercontent.com/dataprofessor/data/master/delaney_solubility_with_descriptors.csv)
""")

# Pandas Profiling Report
if uploaded_file is not None:
    @st.cache
    def load_csv():
        csv = pd.read_csv(uploaded_file, encoding='utf-16', sep='|')
        csv['lat'], csv['lon'] = csv["coordenadas"].str.split(",", 1).str
        csv['lat'] = pd.to_numeric(csv['lat'])
        csv['lon'] = pd.to_numeric(csv['lon'])
        csv = csv.drop(['coordenadas'], axis=1)
        csv = csv.drop(['Unnamed: 0'], axis=1)
        return csv

    df = load_csv()
    pr = ProfileReport(df, explorative=True)
    st.header('**DataFrame.**')
    st.write(df)
    st.write('---')
    st.header('**Reporte de los datos.**')
    st_profile_report(pr)

    #Crear mapa
    st.sidebar.header('2. Crea el mapa de los hoteles.')
    if st.sidebar.checkbox('Mostrar mapa.'):
        map_data = df.iloc[:, -2:]
        st.header('**Ubicaion de los hoteles.**')
        st.map(map_data)
else:
    st.info('Esperando que se cargue el archivo tipo CSV.')
    if st.button('Presiona para usar el Dataset de Ejemplo'):
        # Example data
        @st.cache
        def load_data():
            a = pd.DataFrame(
                np.random.rand(100, 5),
                columns=['a', 'b', 'c', 'd', 'e']
            )
            return a
        df = load_data()
        pr = ProfileReport(df, explorative=True)
        st.header('**DataFrame.**')
        st.write(df)
        st.write('---')
        st.header('**Reporte**')
        st_profile_report(pr)

st.markdown('''
---
**Creditos:** App creada en `Python` + `Streamlit` por la [Secretaria de Administración y Finanzas de la CDMX](https://www.finanzas.cdmx.gob.mx) (aka [SAF](https://www.finanzas.cdmx.gob.mx))
''')