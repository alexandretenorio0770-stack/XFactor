import streamlit as st
import pandas as pd
import utils
import charts


st.set_page_config(page_title="Football Analytics Dashboard", page_icon="⚽", layout="wide")

st.title("⚽ Dashboard de Análise Tática - StatsBomb")
st.markdown("Análise detalhada de dados de evento de partidas de futebol usando `Streamlit`, `mplsoccer` e `StatsBombPy`.")

st.sidebar.header("🔍 Seleção de Partida")

with st.sidebar.spinner("Carregando Competições..."):
    df_comp = utils.load_competitions()

comp_list = df_comp['competition_name'].unique()
selected_comp_name = st.sidebar.selectbox("Selecione o Campeonato:", comp_list)

comp_seasons = df_comp[df_comp['competition_name'] == selected_comp_name]
selected_season_name = st.sidebar.selectbox("Selecione a Temporada:", comp_seasons['season_name'].unique())

comp_id = comp_seasons[comp_seasons['season_name'] == selected_season_name]['competition_id'].values[0]
season_id = comp_seasons[comp_seasons['season_name'] == selected_season_name]['season_id'].values[0]

matches = utils.load_matches(comp_id, season_id)
match_options = {f"{row['home_team']} vs {row['away_team']} ({row['match_date']})": row['match_id'] for _, row in matches.iterrows()}
selected_match_label = st.sidebar.selectbox("Selecione a Partida:", list(match_options.keys()))
match_id = match_options[selected_match_label]

with st.spinner("Carregando dados da partida..."):
    events = utils.load_events(match_id)

summary = utils.get_match_summary(events)

st.subheader("📌 Visão Geral da Partida")
col1, col2, col3, col4 = st.columns(4)

col1.metric(label="Total de Gols", value=summary["total_goals"])
col2.metric(label="Finalizações", value=summary["total_shots"])
col3.metric(label="Passes Totais", value=summary["total_passes"])
col4.metric(label="Precisão de Passes", value=f"{summary['pass_accuracy']}%")

st.divider()

tab1, tab2, tab3 = st.tabs(["📊 Eventos e Métricas", "🎯 Análise Visual (mplsoccer)", "📂 Tabela de Eventos"])

with tab1:
    st.subheader("Filtro Avançado de Jogador")
    
    players = events['player'].dropna().unique()
    selected_player = st.selectbox("Selecione um jogador para análise individual:", ["Todos"] + list(players))
    
    player_filter = None if selected_player == "Todos" else selected_player
    
    if player_filter:
        p_events = events[events['player'] == player_filter]
        p_passes = len(p_events[p_events['type'] == 'Pass'])
        p_shots = len(p_events[p_events['type'] == 'Shot'])
        
        st.info(f"**Estatísticas de {player_filter}:** {p_passes} passes realizados | {p_shots} chutes efetuados.")

with tab2:
    st.subheader("Visualizações Táticas do Campo")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.write("### Mapa de Passes")
        fig_pass = charts.plot_pass_map(events, player_name=player_filter)
        st.pyplot(fig_pass)
        
    with c2:
        st.write("### Mapa de Chutes (xG)")
        fig_shot = charts.plot_shot_map(events)
        st.pyplot(fig_shot)
        
    st.divider()
    st.write("### Densidade de Jogo (Heatmap)")
    fig_heat = charts.plot_pass_heatmap(events)
    st.pyplot(fig_heat)

with tab3:
    st.subheader("Explorador de Dados")
    
    display_cols = [c for c in ['minute', 'second', 'team', 'player', 'type', 'pass_outcome', 'shot_outcome'] if c in events.columns]
    filtered_df = events[display_cols]
    
    st.dataframe(filtered_df, use_container_width=True)
    
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Dados dos Eventos (CSV)",
        data=csv_data,
        file_name=f"eventos_partida_{match_id}.csv",
        mime="text/csv"
    )