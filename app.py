import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Uso diário da Internet por Faixa Etária",
    page_icon="📱",
    layout="centered",

)
st.title("Uso diário da Internet por Faixa Etária 🛜")


df = pd.read_csv("https://raw.githubusercontent.com/Augusto252/uso-di-rio-da-internet-por-faixa-et-ria/refs/heads/main/daily_internet_usage_by_age_group.csv")


st.sidebar.header("Filtros")


# FILTROS

faixa_etaria = sorted(df['age_group'].unique())
faixa_selecionada = st.sidebar.multiselect("Faixa etária", faixa_etaria, default=faixa_etaria)


tempo_rede_social = sorted(df['social_media_hours'].unique())
tempo_rede_social_seleçao = st.sidebar.multiselect("Tempo de uso para rede social", tempo_rede_social, default=tempo_rede_social)


tempo_estudo = sorted(df['work_or_study_hours'].unique())
tempo_estudo_seleçao = st.sidebar.multiselect("Tempo de uso para estudo", tempo_estudo, default=tempo_estudo)


tempo_entreterimento = sorted(df['entertainment_hours'].unique())
tempo_entreterimento_seleçao = st.sidebar.multiselect("Tempo de uso para entreterimento", tempo_entreterimento, default=tempo_entreterimento)


tempo_total = sorted(df['total_screen_time'].unique())
tempo_total_seleçao = st.sidebar.multiselect("Tempo Total", tempo_total, default=tempo_total)


dispositivo = sorted(df['primary_device'].unique())
tipo_dispositivo_seleçao = st.sidebar.multiselect("Tipo de dispositivo", dispositivo, default=dispositivo)


tipo_rede = sorted(df['internet_type'].unique())
tipo_rede_seleçao = st.sidebar.multiselect("Tipo de rede", tipo_rede, default=tipo_rede)



# FILTRAGEM DO DATAFRAME

df_filtrado = df[
    (df['age_group'].isin(faixa_selecionada)) &
    (df['social_media_hours'].isin(tempo_rede_social_seleçao)) &
    (df['work_or_study_hours'].isin(tempo_estudo_seleçao)) &
    (df['entertainment_hours'].isin(tempo_entreterimento_seleçao)) &
    (df['total_screen_time'].isin(tempo_total_seleçao)) &
    (df['primary_device'].isin(tipo_dispositivo_seleçao)) &
    (df['internet_type'].isin(tipo_rede_seleçao))
]


# SUBTÍTULOS/DESCRIÇÕES
st.markdown("Veja o tempo de uso, o tipo de dispositivo, a rede mais acessada e as tarefas realizadas na internet por cada faixa etária. Utilize a barra lateral para selecionar os filtros")

st.subheader("Métricas gerais")



# Métricas Principais
if not df_filtrado.empty:
    tempo_medio = df_filtrado['total_screen_time'].mean()
    tempo_maximo = df_filtrado['total_screen_time'].max()
    dipositivo_mais_usado = df_filtrado["primary_device"].mode()[0]
    idades_mais_recorrentes = df_filtrado["age_group"].mode()[0]

else:
    tempo_medio, tempo_maximo, salario_maximo, total_registros, idades_mais_recorrentes = 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tempo Médio", f"{tempo_medio:,.0f} horas")
col2.metric("Tempo Máximo", f"{tempo_maximo:,.0f} horas")
col3.metric("Dispositivo mais usado", dipositivo_mais_usado)
col4.metric("Faixa etária mais ativa", idades_mais_recorrentes)




# GRÁFICOS
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)


# Top 5 faixas etarias com maior tempo em redes sociais
# Gráfico de barras
with col_graf1:
    if not df_filtrado.empty:
        top_faixas = df_filtrado.groupby('age_group')['social_media_hours'].mean().nlargest(5).sort_values(ascending=True).reset_index()
        grafico_faixas = px.bar(
            top_faixas,
            x='social_media_hours',
            y='age_group',
            orientation='h',
            title="Top 5 mais tempo em redes sociais (por faixa etária)",
            labels={'social_media_hours': "Média de horas por dia", 'age_group': ''}
        )
        grafico_faixas.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_faixas, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")


# Horas de estudo
with col_graf2:
    if not df_filtrado.empty:
        top_faixas = df_filtrado.groupby('age_group')['work_or_study_hours'].mean().nlargest(5).sort_values(ascending=True).reset_index()
        grafico_faixas = px.bar(
            top_faixas,
            x='work_or_study_hours',
            y='age_group',
            orientation='h',
            title="Top 5 mais tempo em trabalho/estudo (por faixa etária)",
            labels={'work_or_study_hours': "Média de horas por dia", 'age_group': ''}
        )
        grafico_faixas.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_faixas, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

col_graf3, col_metrics = st.columns([3,1])

with col_graf3:
    if not df_filtrado.empty:
        top_faixas = df_filtrado.groupby('age_group')['entertainment_hours'].mean().nlargest(5).sort_values(ascending=True).reset_index()
        grafico_faixas = px.bar(
            top_faixas,
            x='entertainment_hours',
            y='age_group',
            orientation='h',
            title="Top 5 mais tempo em entreterimento (por faixa etária)",
            labels={'entertainment_hours': "Média de horas por dia", 'age_group': ''}
        )
        grafico_faixas.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_faixas, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")


# Define metricas em linhas
with col_metrics:
    if not df_filtrado.empty:
        tempo_medio1 = df_filtrado['social_media_hours'].mean()
        tempo_medio2 = df_filtrado['work_or_study_hours'].mean()
        tempo_medio3 = df_filtrado['entertainment_hours'].mean()

        st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
        st.metric("Redes sociais", f"{tempo_medio1:,.0f} horas")
        st.metric("Entrterimento", f"{tempo_medio2:,.0f} horas")
        st.metric("Estudo/Trabalho", f"{tempo_medio3:,.0f} horas")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Nenhum dado encontrado")



col_graf5, col_graf6 = st.columns(2)


# Gráfico de pizza
with col_graf5:
    if not df_filtrado.empty:
        dispositivo_contagem = df_filtrado['primary_device'].value_counts().reset_index()
        dispositivo_contagem.columns = ['tipo_dispositivo', 'quantidade']
        grafico_remoto = px.pie(
            dispositivo_contagem,
            names='tipo_dispositivo',
            values='quantidade',
            title='Proporção dos tipos de dispositivo',
            hole=0.5
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")


# Proporção entre os tipos de rede
with col_graf6:
    if not df_filtrado.empty:
        rede_contagem = df_filtrado['internet_type'].value_counts().reset_index()
        rede_contagem.columns = ['tipo_rede', 'quantidade']
        grafico = px.pie(
            rede_contagem,
            names='tipo_rede',
            values='quantidade',
            title='Proporção dos tipos de rede',
            hole=0.5
        )
        grafico.update_traces(textinfo='percent+label')
        grafico.update_layout(title_x=0.1)
        st.plotly_chart(grafico, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")





