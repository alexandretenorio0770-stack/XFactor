"""
==============================================================================
 PAINEL DE TURISMO DO RIO DE JANEIRO — Data.Rio
==============================================================================
Aplicação Streamlit desenvolvida para o Teste de Performance de 12 itens
sobre desenvolvimento de aplicações com Streamlit.

Fonte dos dados: Portal Data.Rio, seção Turismo
https://www.data.rio/search?groupIds=729990e9fbc04c6ebf81715ab438cae8

Como executar:
    pip install -r requirements.txt
    streamlit run app.py
==============================================================================
"""

import io
import time

import pandas as pd
import plotly.express as px
import streamlit as st

# ------------------------------------------------------------------------
# CONFIGURAÇÃO GERAL DA PÁGINA
# ------------------------------------------------------------------------
st.set_page_config(
    page_title="Turismo no Rio de Janeiro | Data.Rio",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------------
# ITEM 9 — SESSION STATE: inicializa as chaves usadas para persistir
# as preferências do usuário (filtros, seleções e cores) durante a navegação.
# ------------------------------------------------------------------------
DEFAULTS = {
    "df_original": None,
    "bg_color": "#0E1117",
    "font_color": "#FAFAFA",
    "accent_color": "#00C2A8",
    "selected_columns": None,
    "radio_filter_col": None,
    "checkbox_only_numeric": False,
    "dropdown_values": [],
    "sort_col": None,
    "sort_asc": True,
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ------------------------------------------------------------------------
# ITEM 8 — CACHE: evita reprocessar o arquivo XLS a cada interação do usuário.
# A função é "pura" em relação ao conteúdo do arquivo (cacheada pelo hash
# dos bytes enviados), então só é reexecutada se um novo arquivo for enviado.
# ------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def carregar_xls(arquivo_bytes: bytes) -> pd.DataFrame:
    """Lê um arquivo XLS/XLSX em memória e devolve um DataFrame."""
    return pd.read_excel(io.BytesIO(arquivo_bytes))


@st.cache_data(show_spinner=False)
def converter_para_xlsx(df: pd.DataFrame) -> bytes:
    """Converte um DataFrame para bytes de um arquivo XLSX (para download)."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="dados_filtrados")
    return buffer.getvalue()


# ------------------------------------------------------------------------
# ITEM 7 — COLOR PICKER: personalização visual do painel
# ------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Configurações")

    st.subheader("🎨 Personalização")
    st.session_state.bg_color = st.color_picker(
        "Cor de fundo do painel", st.session_state.bg_color
    )
    st.session_state.font_color = st.color_picker(
        "Cor da fonte", st.session_state.font_color
    )
    st.session_state.accent_color = st.color_picker(
        "Cor de destaque (gráficos e botões)", st.session_state.accent_color
    )

# CSS dinâmico aplicando as cores escolhidas pelo usuário
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {st.session_state.bg_color};
            color: {st.session_state.font_color};
        }}
        h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {{
            color: {st.session_state.font_color} !important;
        }}
        div.stButton > button, div.stDownloadButton > button {{
            background-color: {st.session_state.accent_color};
            color: #0E1117;
            border: none;
            font-weight: 600;
            border-radius: 8px;
        }}
        [data-testid="stMetricValue"] {{
            color: {st.session_state.accent_color} !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------------
# CABEÇALHO E ITEM 1 — OBJETIVO E MOTIVAÇÃO
# ------------------------------------------------------------------------
st.title("🌴 Painel de Turismo do Rio de Janeiro")
st.caption("Fonte: Portal Data.Rio — seção Turismo")

with st.expander("📌 Item 1 — Objetivo, motivação e datasets escolhidos", expanded=True):
    st.markdown(
        """
        **Datasets sugeridos (portal Data.Rio – Turismo):**
        - Desembarques de passageiros no Aeroporto Internacional do Galeão / Santos Dumont
        - Chegada de turistas ao Rio de Janeiro por via aérea, marítima e rodoviária
        - Ocupação hoteleira e número de estabelecimentos de hospedagem
        - Movimento de cruzeiros marítimos no Porto do Rio

        **Objetivo:** oferecer um painel interativo que permita à Secretaria de
        Turismo, pesquisadores e ao público em geral explorar, filtrar e
        visualizar rapidamente indicadores de fluxo turístico da cidade,
        identificando sazonalidades, meios de transporte mais utilizados e
        tendências de crescimento/queda ao longo do tempo.

        **Motivação:** dados de turismo abertos costumam estar dispersos em
        múltiplas planilhas, dificultando análises rápidas. Uma interface
        única, com filtros, gráficos e exportação de dados, agiliza a tomada
        de decisão e a comunicação de resultados.

        **Funcionalidades implementadas:** upload de arquivo XLS, filtros
        (radio, checkbox e dropdown), tabela interativa ordenável, download
        dos dados filtrados, barra de progresso/spinner, personalização de
        cores, cache de dados, persistência de preferências via Session
        State, gráficos simples (barra, linha, pizza), gráficos avançados
        (histograma e dispersão) e métricas resumo.
        """
    )

st.divider()

# ------------------------------------------------------------------------
# ITEM 2 — UPLOAD DE ARQUIVO XLS
# ------------------------------------------------------------------------
st.header("📂 Item 2 — Upload do arquivo de dados")
arquivo = st.file_uploader(
    "Envie um arquivo XLS/XLSX de turismo baixado do portal Data.Rio",
    type=["xls", "xlsx"],
)

if arquivo is None:
    st.info(
        "Aguardando o envio de um arquivo XLS/XLSX. "
        "Baixe um dataset em https://www.data.rio/search?groupIds=729990e9fbc04c6ebf81715ab438cae8 "
        "e envie-o acima para habilitar toda a aplicação."
    )
    st.stop()

# ------------------------------------------------------------------------
# ITEM 6 — BARRA DE PROGRESSO E SPINNER durante o carregamento
# ------------------------------------------------------------------------
with st.spinner("Processando o arquivo XLS..."):
    progresso = st.progress(0, text="Lendo arquivo...")
    for pct in (20, 45, 70):
        time.sleep(0.05)
        progresso.progress(pct, text="Lendo arquivo...")

    df = carregar_xls(arquivo.getvalue())
    st.session_state.df_original = df

    progresso.progress(100, text="Concluído!")
    time.sleep(0.15)
    progresso.empty()

st.success(f"Arquivo carregado com sucesso — {df.shape[0]} linhas e {df.shape[1]} colunas.")

# ------------------------------------------------------------------------
# ITEM 3 — FILTROS: radio, checkbox e dropdown (multiselect)
# ------------------------------------------------------------------------
st.header("🔎 Item 3 — Filtros e seleção de dados")

todas_colunas = list(df.columns)
colunas_numericas = df.select_dtypes(include="number").columns.tolist()
colunas_categoricas = [c for c in todas_colunas if c not in colunas_numericas]

col_a, col_b, col_c = st.columns(3)

# --- RADIO: escolher a coluna categórica usada para filtrar linhas ---
with col_a:
    opcoes_radio = ["(nenhuma)"] + colunas_categoricas
    default_idx = (
        opcoes_radio.index(st.session_state.radio_filter_col)
        if st.session_state.radio_filter_col in opcoes_radio
        else 0
    )
    coluna_filtro = st.radio(
        "Filtrar linhas pela coluna:",
        opcoes_radio,
        index=default_idx,
        help="Selecione uma coluna categórica para filtrar as linhas do dataset.",
    )
    st.session_state.radio_filter_col = coluna_filtro

# --- DROPDOWN (multiselect): valores da coluna escolhida no radio ---
with col_b:
    if coluna_filtro != "(nenhuma)":
        valores_disponiveis = sorted(df[coluna_filtro].dropna().astype(str).unique().tolist())
        default_vals = [v for v in st.session_state.dropdown_values if v in valores_disponiveis]
        valores_selecionados = st.multiselect(
            f"Valores de '{coluna_filtro}' a incluir:",
            valores_disponiveis,
            default=default_vals if default_vals else valores_disponiveis,
        )
        st.session_state.dropdown_values = valores_selecionados
    else:
        valores_selecionados = None
        st.caption("Selecione uma coluna no filtro de rádio para habilitar o dropdown.")

# --- CHECKBOX: exibir apenas colunas numéricas junto às categóricas-chave ---
with col_c:
    st.session_state.checkbox_only_numeric = st.checkbox(
        "Mostrar apenas colunas numéricas (+ colunas de filtro)",
        value=st.session_state.checkbox_only_numeric,
    )

# Seleção explícita de colunas a exibir
if st.session_state.selected_columns is None:
    st.session_state.selected_columns = todas_colunas

colunas_para_exibir = st.multiselect(
    "Colunas a exibir na tabela e nos gráficos:",
    todas_colunas,
    default=[c for c in st.session_state.selected_columns if c in todas_colunas] or todas_colunas,
)
st.session_state.selected_columns = colunas_para_exibir

# Aplica os filtros
df_filtrado = df.copy()
if coluna_filtro != "(nenhuma)" and valores_selecionados:
    df_filtrado = df_filtrado[df_filtrado[coluna_filtro].astype(str).isin(valores_selecionados)]

colunas_finais = colunas_para_exibir
if st.session_state.checkbox_only_numeric:
    colunas_finais = [c for c in colunas_para_exibir if c in colunas_numericas or c == coluna_filtro]
    if not colunas_finais:
        colunas_finais = colunas_para_exibir

if colunas_finais:
    df_filtrado = df_filtrado[colunas_finais]

st.divider()

# ------------------------------------------------------------------------
# ITEM 4 — TABELA INTERATIVA (ordenável e filtrável pela própria interface)
# ------------------------------------------------------------------------
st.header("📋 Item 4 — Tabela interativa")

col_sort1, col_sort2 = st.columns([3, 1])
with col_sort1:
    colunas_disponiveis_sort = df_filtrado.columns.tolist()
    if colunas_disponiveis_sort:
        default_sort = (
            st.session_state.sort_col
            if st.session_state.sort_col in colunas_disponiveis_sort
            else colunas_disponiveis_sort[0]
        )
        sort_col = st.selectbox("Ordenar por:", colunas_disponiveis_sort, index=colunas_disponiveis_sort.index(default_sort))
        st.session_state.sort_col = sort_col
with col_sort2:
    sort_asc = st.toggle("Crescente", value=st.session_state.sort_asc)
    st.session_state.sort_asc = sort_asc

if not df_filtrado.empty and st.session_state.sort_col in df_filtrado.columns:
    df_filtrado = df_filtrado.sort_values(by=st.session_state.sort_col, ascending=sort_asc)

st.dataframe(
    df_filtrado,
    use_container_width=True,
    height=380,
    hide_index=True,
)
st.caption(
    "Dica: clique no cabeçalho de qualquer coluna na tabela acima para "
    "ordenar/filtrar diretamente pela interface nativa do Streamlit."
)

# ------------------------------------------------------------------------
# ITEM 5 — DOWNLOAD DOS DADOS FILTRADOS EM XLS
# ------------------------------------------------------------------------
st.header("⬇️ Item 5 — Download dos dados filtrados")
xlsx_bytes = converter_para_xlsx(df_filtrado)
st.download_button(
    label="Baixar dados filtrados (.xlsx)",
    data=xlsx_bytes,
    file_name="turismo_rio_filtrado.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

st.divider()

# ------------------------------------------------------------------------
# ITEM 12 — MÉTRICAS BÁSICAS
# ------------------------------------------------------------------------
st.header("📊 Item 12 — Métricas resumo")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Registros filtrados", f"{df_filtrado.shape[0]:,}".replace(",", "."))
m2.metric("Colunas exibidas", df_filtrado.shape[1])

colunas_numericas_filtrado = df_filtrado.select_dtypes(include="number").columns.tolist()
if colunas_numericas_filtrado:
    col_metric = colunas_numericas_filtrado[0]
    m3.metric(f"Média de {col_metric}", f"{df_filtrado[col_metric].mean():,.2f}")
    m4.metric(f"Soma de {col_metric}", f"{df_filtrado[col_metric].sum():,.2f}")
else:
    m3.metric("Média", "—")
    m4.metric("Soma", "—")

st.divider()

# ------------------------------------------------------------------------
# ITEM 10 — GRÁFICOS SIMPLES (barra, linha e pizza)
# ------------------------------------------------------------------------
st.header("📈 Item 10 — Gráficos simples")

if colunas_numericas_filtrado and colunas_categoricas:
    col_g1, col_g2 = st.columns(2)

    eixo_x = st.selectbox(
        "Coluna categórica (eixo X / categorias):",
        [c for c in colunas_categoricas if c in df_filtrado.columns] or todas_colunas,
        key="eixo_x_simples",
    )
    eixo_y = st.selectbox(
        "Coluna numérica (eixo Y / valores):", colunas_numericas_filtrado, key="eixo_y_simples"
    )

    dados_agg = df_filtrado.groupby(eixo_x, as_index=False)[eixo_y].sum()

    with col_g1:
        fig_bar = px.bar(
            dados_agg, x=eixo_x, y=eixo_y, title=f"{eixo_y} por {eixo_x} (barras)",
            color_discrete_sequence=[st.session_state.accent_color],
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        fig_pizza = px.pie(
            dados_agg, names=eixo_x, values=eixo_y, title=f"Participação de {eixo_x} em {eixo_y}",
        )
        st.plotly_chart(fig_pizza, use_container_width=True)

    with col_g2:
        fig_linha = px.line(
            dados_agg, x=eixo_x, y=eixo_y, title=f"{eixo_y} ao longo de {eixo_x} (linha)", markers=True,
            color_discrete_sequence=[st.session_state.accent_color],
        )
        st.plotly_chart(fig_linha, use_container_width=True)
else:
    st.warning("São necessárias ao menos uma coluna numérica e uma categórica para gerar estes gráficos.")

st.divider()

# ------------------------------------------------------------------------
# ITEM 11 — GRÁFICOS AVANÇADOS (histograma e dispersão)
# ------------------------------------------------------------------------
st.header("🔬 Item 11 — Gráficos avançados")

if len(colunas_numericas_filtrado) >= 1:
    col_h1, col_h2 = st.columns(2)

    with col_h1:
        col_hist = st.selectbox("Coluna para o histograma:", colunas_numericas_filtrado, key="hist_col")
        fig_hist = px.histogram(
            df_filtrado, x=col_hist, nbins=30, title=f"Distribuição de {col_hist}",
            color_discrete_sequence=[st.session_state.accent_color],
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_h2:
        if len(colunas_numericas_filtrado) >= 2:
            col_x = st.selectbox("Eixo X (dispersão):", colunas_numericas_filtrado, index=0, key="scatter_x")
            col_y = st.selectbox(
                "Eixo Y (dispersão):", colunas_numericas_filtrado,
                index=min(1, len(colunas_numericas_filtrado) - 1), key="scatter_y",
            )
            cor_opcional = None
            if coluna_filtro != "(nenhuma)" and coluna_filtro in df.columns:
                cor_opcional = coluna_filtro if coluna_filtro in df_filtrado.reset_index().columns else None
            fig_scatter = px.scatter(
                df_filtrado, x=col_x, y=col_y, title=f"{col_y} vs. {col_x} (dispersão)",
                color_discrete_sequence=[st.session_state.accent_color],
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("São necessárias ao menos duas colunas numéricas para o gráfico de dispersão.")
else:
    st.warning("Nenhuma coluna numérica disponível para gerar gráficos avançados.")

st.divider()
st.caption(
    "Desenvolvido com Streamlit • Dados: Portal Data.Rio (seção Turismo) • "
    "Uso de IA declarado conforme política Sinal Verde 🟢"
)
