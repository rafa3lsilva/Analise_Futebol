import streamlit as st

def sidebar(home_team, away_team):
    # st.sidebar.header("📊 Análise de Jogos de Futebol")
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
    st.sidebar.markdown("<br>", unsafe_allow_html=True)


def btts_over(btts_status, over_status, btts_home, btts_away, over_home, over_away):
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
