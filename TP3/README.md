# Painel de Turismo do Rio de Janeiro — Streamlit + Data.Rio

Aplicação Streamlit desenvolvida para o teste de performance de 12 itens
sobre desenvolvimento de aplicações com Streamlit, usando dados do portal
[Data.Rio — seção Turismo](https://www.data.rio/search?groupIds=729990e9fbc04c6ebf81715ab438cae8).

## Como executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

Depois, na interface, faça upload de um arquivo `.xls`/`.xlsx` de turismo
baixado do portal Data.Rio (ex.: desembarques de passageiros, chegada de
turistas, ocupação hoteleira, movimento de cruzeiros).

## Mapeamento dos itens no código (`app.py`)

| Item | Competência | Onde está |
|---|---|---|
| 1 | Objetivo e motivação dos datasets | Bloco `st.expander("📌 Item 1 ...")` |
| 2 | Upload de arquivo XLS | `st.file_uploader` |
| 3 | Filtros (radio, checkbox, dropdown) | Seção "Item 3" |
| 4 | Tabela interativa ordenável | `st.dataframe` + seletor de ordenação |
| 5 | Download dos dados filtrados | `st.download_button` + `converter_para_xlsx` |
| 6 | Barra de progresso e spinner | `st.spinner` + `st.progress` no carregamento |
| 7 | Color picker | `st.color_picker` na barra lateral + CSS dinâmico |
| 8 | Cache | `@st.cache_data` em `carregar_xls` e `converter_para_xlsx` |
| 9 | Session State | `st.session_state` inicializado no topo e usado nos filtros/cores |
| 10 | Gráficos simples (barra, linha, pizza) | Seção "Item 10" com Plotly Express |
| 11 | Gráficos avançados (histograma, dispersão) | Seção "Item 11" com Plotly Express |
| 12 | Métricas básicas | Seção "Item 12" com `st.metric` |

## Sobre o uso de IA (Sinal Verde 🟢)

Este projeto foi desenvolvido com o apoio de uma ferramenta de IA
(Claude, da Anthropic), utilizada para gerar a estrutura inicial do
código Streamlit e redigir a
documentação. Conforme a política "Sinal Verde", essa citação é feita
para declarar o uso da ferramenta. 
