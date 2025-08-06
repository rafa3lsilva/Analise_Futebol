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
    #st.write(df)

    #filtro para a média de gols do home
    df_home_media = df.iloc[0:6]

    #filtro para exibir os últimos jogos (Home)
    df_home = df.iloc[0:6]
    flt_home = pd.DataFrame({"Data": df_home["Data"],
                             "Competição": df_home["Competição"],
                             "Time A": df_home["Time A"],
                             "Time B": df_home["Time B"],
                             "Gols A": df_home["Gols A"],
                             "Gols B": df_home["Gols B"],
                             "Resultado": df_home["Resultado"]})

    st.subheader("Últimos Jogos (Home)")
    st.dataframe(drop_reset_index(flt_home))

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

    st.write(f"⚽ Média de gols marcados: {media_marcados:.2f}")
    st.write(f"🛡️ Média de gols sofridos: {media_sofridos:.2f}")


    # filtro para a média de gols do Away
    df_away_media = df.iloc[10:16]

    # filtro para exibir os últimos jogos (Away)
    df_away = df.iloc[10:16]
    flt_away = pd.DataFrame({"Data": df_away["Data"],
                             "Competição": df_away["Competição"],
                             "Time A": df_away["Time A"],
                             "Time B": df_away["Time B"],
                             "Gols A": df_away["Gols A"],
                             "Gols B": df_away["Gols B"],
                             "Resultado": df_away["Resultado"]})
    st.subheader("Últimos Jogos (Away)")
    st.dataframe(drop_reset_index(flt_away))

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

    st.write(f"⚽ Média de gols marcados (Away): {media_marcados:.2f}")
    st.write(f"🛡️ Média de gols sofridos (Away): {media_sofridos:.2f}")


# Verifica se os DataFrames existem e não estão vazios
if "df_home_media" in locals() and not df_home_media.empty and \
   "df_away_media" in locals() and not df_away_media.empty:

    # Calcula as médias com fallback para zero se estiverem vazias
    media_home_marcados = df_home_media["Gols Marcados"].mean() or 0
    media_home_sofridos = df_home_media["Gols Sofridos"].mean() or 0
    media_away_marcados = df_away_media["Gols Marcados"].mean() or 0
    media_away_sofridos = df_away_media["Gols Sofridos"].mean() or 0

    # Dados para o gráfico
    categorias = ["Gols Marcados", "Gols Sofridos"]
    valores_home = [media_home_marcados, media_home_sofridos]
    valores_away = [media_away_marcados, media_away_sofridos]
    x = range(len(categorias))

    # Gráfico
    fig, ax = plt.subplots()
    ax.bar([i - 0.2 for i in x], valores_home,
           width=0.4, label="Home", color="#1f77b4")
    ax.bar([i + 0.2 for i in x], valores_away,
           width=0.4, label="Away", color="#ff7f0e")

    ax.set_xticks(x)
    ax.set_xticklabels(categorias)
    ax.set_ylabel("Média de Gols")
    ax.set_title("Comparação de Gols: Home vs Away")
    ax.legend()

    st.pyplot(fig)

else:
    st.warning(
        "⚠️ Dados insuficientes para gerar o gráfico. Verifique se os DataFrames foram carregados corretamente.")
