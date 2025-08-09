import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import re
import data
import sidebar


def drop_reset_index(df):
    df = df.dropna()
    df = df.reset_index(drop=True)
    df.index += 1
    return df


# Função para configurar a página Streamlit
def configurar_pagina():
    st.set_page_config(
        page_title="Análise Futebol",
        page_icon=":soccer:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

configurar_pagina()

# Título da página
st.markdown("<h1 style='text-align: center;'>📊 Análise de Jogos de Futebol</h1>", unsafe_allow_html=True)

# Descrição
st.markdown("""
<div  style="text-align: center; font-size: 16px;">
    <p style='text-align: center;'>Esta é uma aplicação para análise de jogos de futebol usando dados do site Flashscore.</p>
    <p style='text-align: center;'>Você pode fazer upload de arquivos .txt com os dados dos jogos e obter análises detalhadas.</p>
    <p style='text-align: center;'>Para mais informações, consulte o tutorial na barra lateral.</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("📊 Análise de Jogos de Futebol")
# Tutorial
tutorial_url = "https://www.notion.so/Tutorial-Flashscore-2484bab1283b80f4b051e65d782a19d5?source=copy_link"

st.sidebar.markdown(f"""
    <div style="text-align: center; font-size: 16px;">
        <a href="{tutorial_url}" target="_blank" style="text-decoration: none;">
            <div style="margin-bottom: 10px; background-color:#1f77b4; padding:8px; border-radius:6px; color:white;">
                📚 Tutorial
            </div>
        </a>
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

df = data.processar_dados()
if 'Data' in df.columns:
    home_team = df["Time Referência"].unique()[0] if not df.empty else 'Home'
    away_team = df["Time Referência"].unique()[1] if not df.empty else 'Away'

    sidebar.sidebar(home_team, away_team)

    # Seleção do intervalo de jogos com visual aprimorado
    st.markdown(
        "<h3 style='text-align: Left; color: #1f77b4;margin-bottom: -50px'>Selecione o intervalo de jogos:</h3>",
        unsafe_allow_html=True
    )
    intervalo = st.radio(
        "",
        options=["Últimos 5 jogos", "Últimos 6 jogos", "Últimos 9 jogos", "Últimos 10 jogos"],
        index=0,
        horizontal=True,
        key="intervalo_radio"
    )

    # Extrai o número do texto selecionado
    num_jogos = int(intervalo.split()[1])  # pega o número após "Últimos"

    # Aplica o intervalo nos DataFrames
    df_home_media = df.iloc[0:num_jogos]
    df_away_media = df.iloc[10:10 + num_jogos]

    #filtro para exibir os últimos jogos (Home)

    df_home = df.iloc[0:num_jogos]
    flt_home = pd.DataFrame({"Data": df_home["Data"],
                                "Competição": df_home["Competição"],
                                "Time A": df_home["Time A"],
                                "Time B": df_home["Time B"],
                                "Gols A": df_home["Gols A"],
                                "Gols B": df_home["Gols B"],
                                "Resultado": df_home["Resultado"]})


    # Cálculo da posição (Home/Away) — feito uma única vez
    df_home_media["Local"] = df_home_media.apply(
        lambda row: "Home" if row["Time Referência"] == row["Time A"] else
                    "Away" if row["Time Referência"] == row["Time B"] else
                    None,
        axis=1
    )

    # Gols marcados pelo time de referência
    df_home_media["Gols Marcados"] = df_home_media.apply(
        lambda row: row["Gols A"] if row["Local"] == "Home" else
        row["Gols B"] if row["Local"] == "Away" else
        None,
        axis=1
    )

    # Gols sofridos pelo time de referência
    df_home_media["Gols Sofridos"] = df_home_media.apply(
        lambda row: row["Gols B"] if row["Local"] == "Home" else
        row["Gols A"] if row["Local"] == "Away" else
        None,
        axis=1
    )

    # Exibe as médias
    media_marcados = df_home_media["Gols Marcados"].mean()
    media_sofridos = df_home_media["Gols Sofridos"].mean()

    # filtro para exibir os últimos jogos (Away)
    df_away = df.iloc[10:10 + num_jogos:]
    flt_away = pd.DataFrame({"Data": df_away["Data"],
                                "Competição": df_away["Competição"],
                                "Time A": df_away["Time A"],
                                "Time B": df_away["Time B"],
                                "Gols A": df_away["Gols A"],
                                "Gols B": df_away["Gols B"],
                                "Resultado": df_away["Resultado"]})

    # Cálculo da posição (Home/Away) — feito uma única vez
    df_away_media["Local"] = df_away_media.apply(
        lambda row: "Home" if row["Time Referência"] == row["Time A"] else
                    "Away" if row["Time Referência"] == row["Time B"] else
                    None,
        axis=1
    )

    # Gols marcados pelo time de referência
    df_away_media["Gols Marcados"] = df_away_media.apply(
        lambda row: row["Gols A"] if row["Local"] == "Home" else
        row["Gols B"] if row["Local"] == "Away" else
        None,
        axis=1
    )

    # Gols sofridos pelo time de referência
    df_away_media["Gols Sofridos"] = df_away_media.apply(
        lambda row: row["Gols B"] if row["Local"] == "Home" else
        row["Gols A"] if row["Local"] == "Away" else
        None,
        axis=1
    )

    # Exibe as médias
    media_marcados = df_away_media["Gols Marcados"].mean()
    media_sofridos = df_away_media["Gols Sofridos"].mean()

    # Verifica se os DataFrames existem e não estão vazios
    if "df_home_media" in locals() and not df_home_media.empty and \
    "df_away_media" in locals() and not df_away_media.empty:

        # Calcula as médias com fallback para zero se estiverem vazias
        media_home_marcados = df_home_media["Gols Marcados"].mean() or 0
        media_home_sofridos = df_home_media["Gols Sofridos"].mean() or 0
        media_away_marcados = df_away_media["Gols Marcados"].mean() or 0
        media_away_sofridos = df_away_media["Gols Sofridos"].mean() or 0


    st.markdown("### 📋 Médias de Gols", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display: flex; justify-content: space-around;">
        <div style="background-color:#1f77b4; padding:15px; border-radius:8px; width:45%; text-align:center; color:white;">
            <h3>🏠 {home_team}</h3>
            <p style="font-size:18px;">⚽ Média de Gols Marcados: <strong>{media_home_marcados:.2f}</strong></p>
            <p style="font-size:18px;">🛡️ Média de Gols Sofridos: <strong>{media_home_sofridos:.2f}</strong></p>
        </div>
        <div style="background-color:#d62728; padding:15px; border-radius:8px; width:45%; text-align:center; color:white;">
            <h3>✈️ {away_team}</h3>
            <p style="font-size:18px;">⚽ Média de Gols Marcados: <strong>{media_away_marcados:.2f}</strong></p>
            <p style="font-size:18px;">🛡️ Média de Gols Sofridos: <strong>{media_away_sofridos:.2f}</strong></p>
        </div>
    </div>
        """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # criando o metodo para BTTS
    # Garantindo que as médias sejam numéricas

    btts_home = (media_home_marcados + media_away_sofridos) / 2
    btts_away = (media_away_marcados + media_home_sofridos) / 2


    def btts_status(btts_home, btts_away):
        if btts_home > 1.4 and btts_away > 1.4:
            return "🟢 Alta chance"
        elif btts_home > 1.2 and btts_away > 1.2:
            return "🟡 Moderada"
        else:
            return "🔴 Baixa"

    # criando o metodo para Over 2.5 Gols
    over_home = (media_home_marcados + media_away_sofridos) / 2
    over_away = (media_away_marcados + media_home_sofridos) / 2

    def over_status(over_home, over_away):
        if over_home > 1.66 and over_away > 1.66:
            return "🟢 Alta chance"
        elif over_home > 1.4 and over_away > 1.4:
            return "🟡 Moderada"
        else:
            return "🔴 Baixa"

    sidebar.btts_over(btts_status, over_status, btts_home, btts_away, over_home, over_away)

    # Exibe os últimos jogos (Home)
    st.subheader(f"Últimos {num_jogos} jogos do {home_team}")
    st.dataframe(drop_reset_index(flt_home))
    # Exibe os últimos jogos (Away)
    st.subheader(f"Últimos {num_jogos} jogos do {away_team}")
    st.dataframe(drop_reset_index(flt_away))