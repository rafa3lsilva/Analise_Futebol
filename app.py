import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import re


def drop_reset_index(df):
    df = df.dropna()
    df = df.reset_index(drop=True)
    df.index += 1
    return df


st.title("📊 Análise de Jogos de Futebol")

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
st.sidebar.markdown("---")

# Inicializa o estado
if "dados_jogos" not in st.session_state:
    st.session_state.dados_jogos = None

# Botão para reiniciar
if st.session_state.dados_jogos:
    if st.button("🔄 Novo Arquivo"):
        st.session_state.dados_jogos = None
        st.rerun()

# Upload do arquivo (só aparece se ainda não foi carregado)
if not st.session_state.dados_jogos:
    uploaded_file = st.file_uploader(
        "Escolha o arquivo .txt com os dados dos jogos", type="txt")

    if uploaded_file:
        linhas = uploaded_file.read().decode("utf-8").splitlines()
        linhas = [linha.strip() for linha in linhas if linha.strip()]
        st.session_state.dados_jogos = linhas
        st.rerun()

# Processamento dos dados (só se o arquivo foi carregado)
if st.session_state.dados_jogos:
    linhas = st.session_state.dados_jogos
    jogos = []
    i = 0
    time_referencia = None

    while i < len(linhas):
        if linhas[i].startswith("Últimos jogos:"):
            time_referencia = linhas[i].split(":")[1].strip()
            i += 1
            continue

        if time_referencia is None:
            i += 1
            continue

        if i + 6 >= len(linhas):
            break

        try:
            data = linhas[i]
            competencia = linhas[i+1]
            time_a = linhas[i+2]
            time_b = linhas[i+3]

            if (i + 8 < len(linhas) and
                re.match(r"^\d+$", linhas[i+4]) and
                re.match(r"^\d+$", linhas[i+5]) and
                re.match(r"^\d+$", linhas[i+6]) and
                    re.match(r"^\d+$", linhas[i+7])):
                gols_a = int(linhas[i+6])
                gols_b = int(linhas[i+7])
                resultado_original = linhas[i+8]
                i += 9
            else:
                gols_a = int(linhas[i+4])
                gols_b = int(linhas[i+5])
                resultado_original = linhas[i+6]
                i += 7

            if gols_a > gols_b:
                resultado_corrigido = "V"
            elif gols_a < gols_b:
                resultado_corrigido = "D"
            else:
                resultado_corrigido = "E"

            jogo = {
                "Time Referência": time_referencia,
                "Data": data,
                "Competição": competencia,
                "Time A": time_a,
                "Time B": time_b,
                "Gols A": gols_a,
                "Gols B": gols_b,
                "Resultado": resultado_corrigido
            }

            jogos.append(jogo)

        except (IndexError, ValueError):
            i += 1

    df = pd.DataFrame(jogos)

    home_team = df["Time Referência"].unique()[0] if not df.empty else 'Home'
    away_team = df["Time Referência"].unique()[1] if not df.empty else 'Away'

    #st.sidebar.header("📊 Análise de Jogos de Futebol")
    st.sidebar.write("### Confronto:")

    # Layout vertical centralizado
    st.sidebar.markdown(f"""
        <div style="text-align: center; font-size: 16px;">
            <div style="margin-bottom: 10px; background-color:#1f77b4; padding:8px; border-radius:6px; color:white;">
                🏠 {home_team}
            </div>
            <div style="margin-bottom: 5px;">⚔️ vs</div>
            <div style="background-color:#d62728; padding:8px; border-radius:6px; color:white;">
                ✈️ {away_team}
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    # Seleção do intervalo de jogos
    intervalo = st.radio("Selecione o intervalo de jogos:",
             options=["Últimos 5 jogos", "Últimos 6 jogos", "Últimos 9 jogos", "Últimos 10 jogos"],
             index=0,
             horizontal=True)

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

    
    st.markdown("### 📋 Médias de Gols Home e Away", unsafe_allow_html=True)

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
    st.markdown("---")

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

    # Exibe os indicadores na sidebar
   
    st.sidebar.markdown("### 🎯 Indicadores da Partida")

    # Card BTTS
    st.sidebar.markdown(f"""
        <div style="background-color:#262730; padding:10px; border-radius:8px; text-align:center;">
            <span style="font-size:16px; font-weight:bold; color:white;">🔍 BTTS (Ambas Marcam)</span><br>
            <span style="font-size:20px; font-weight:bold; color:white;">{btts_home:.2f}</span><br>
            <span style="font-size:16px;">{btts_status(btts_home, btts_away)}</span>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("")

    # Card Over 2.5
    st.sidebar.markdown(f"""
        <div style="background-color:#262730; padding:10px; border-radius:8px; text-align:center;">
            <span style="font-size:16px; font-weight:bold; color:white;">🔍 Over 2.5 Gols</span><br>
            <span style="font-size:20px; font-weight:bold; color:white;">{over_home:.2f}</span><br>
            <span style="font-size:16px;">{over_status(over_home, over_away)}</span>
        </div>
    """, unsafe_allow_html=True)

    # Exibe os últimos jogos (Home)
    st.subheader("Últimos Jogos (Home)")
    st.dataframe(drop_reset_index(flt_home))
    # Exibe os últimos jogos (Away)
    st.subheader("Últimos Jogos (Away)")
    st.dataframe(drop_reset_index(flt_away))