# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="Dashboard Interativo",
    page_icon="📊",
    layout="wide"
)

# Função para carregar dados
@st.cache_data
def load_data():
    # URL original convertida para download direto
    url = "https://gvmail-my.sharepoint.com/:x:/g/personal/c3007596_fgv_edu_br/ERkvqr-gd-lBlzJPUMarJ1cBo2IP_j0kCzea6SrFKD_oIg?e=R1B0Tq&download=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = pd.read_excel(BytesIO(response.content))
        return data
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

# Carregar dados
df = load_data()

if df is not None:
    # Sidebar
    st.sidebar.title("⚙️ Configurações")
    
    # Seletores
    colunas_numericas = df.select_dtypes(include=['number']).columns
    colunas_categoricas = df.select_dtypes(include=['object']).columns
    
    # Widgets interativos
    x_axis = st.sidebar.selectbox("Eixo X", colunas_numericas)
    y_axis = st.sidebar.selectbox("Eixo Y", colunas_numericas)
    categoria = st.sidebar.selectbox("Categoria", colunas_categoricas)

    # Layout principal
    st.title("📈 Dashboard Analítico Interativo")
    st.markdown("---")

    # Métricas principais
    st.subheader("📊 Métricas Principais")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total de Registros",
            value=len(df),
            delta=f"{len(df.columns)} colunas"
        )
    
    with col2:
        st.metric(
            label=f"Soma de {y_axis}",
            value=f"{df[y_axis].sum():.2f}",
            delta=f"Média: {df[y_axis].mean():.2f}"
        )
    
    with col3:
        st.metric(
            label=f"Maior {x_axis}",
            value=f"{df[x_axis].max():.2f}",
            delta=f"Menor: {df[x_axis].min():.2f}"
        )

    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Gráfico de Barras")
        fig_bar = px.bar(
            df,
            x=x_axis,
            y=y_axis,
            color=categoria,
            barmode="group"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("🫀 Gráfico de Dispersão")
        fig_scatter = px.scatter(
            df,
            x=x_axis,
            y=y_axis,
            color=categoria,
            size=y_axis,
            hover_data=[x_axis]
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Tabela interativa
    st.subheader("📋 Dados Brutos")
    st.dataframe(df, use_container_width=True)

else:
    st.error("❌ Não foi possível carregar os dados. Verifique a conexão com a fonte.")
