import pandas as pd
import streamlit as st
import re

def drop_reset_index(df):
    df = df.dropna()
    df = df.reset_index(drop=True)
    df.index += 1
    return df

def processar_dados():
    # Inicializa o estado
    if "dados_jogos" not in st.session_state:
        st.session_state.dados_jogos = None

    # Botão para reiniciar
    if st.session_state.dados_jogos:
        if st.sidebar.button("🔄 Novo Arquivo"):
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

    jogos = []
    # Processamento dos dados (só se o arquivo foi carregado)
    if st.session_state.dados_jogos:
        linhas = st.session_state.dados_jogos
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

    df = drop_reset_index(df)

    return df
