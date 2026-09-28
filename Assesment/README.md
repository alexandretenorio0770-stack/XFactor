# ⚽ Football Analytics Dashboard - Guia de Uso

Este projeto é um dashboard interativo desenvolvido em **Python** utilizando **Streamlit**, **StatsBombPy** e **mplsoccer**. O objetivo da aplicação é permitir a análise tática e estatística de partidas de futebol a partir de dados reais da base aberta da **StatsBomb**.

---

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:
* **Python** (versão 3.9 ou superior)
* **Git** (para clonar o repositório)

---

## ⚙️ Instalação e Execução Local

Siga os passos abaixo para rodar a aplicação em seu ambiente local:

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/football-analytics-dashboard.git
cd football-analytics-dashboard
```

### 2. Criar e ativar o ambiente virtual

* **No Linux/macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

* **No Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação Streamlit
```bash
streamlit run app.py
```
O dashboard será aberto automaticamente no seu navegador no endereço `http://localhost:8501`.

---

## 🚀 Como Utilizar o Dashboard

O painel está estruturado para proporcionar uma navegação fluida e intuitiva:

### 1. Painel Lateral (Sidebar) — Seleção de Partidas
1. **Campeonato:** Escolha a competição desejada na caixa de seleção (ex: *La Liga*, *Champions League*, *FIFA World Cup*).
2. **Temporada:** Escolha o ano/temporada da competição.
3. **Partida:** Selecione o jogo específico que deseja analisar. Os dados serão carregados automaticamente.

### 2. Visão Geral (Métricas)
No topo da página principal, você visualizará quatro cards de métricas (*metrics*) com os dados gerais do confronto:
* Total de Gols
* Total de Finalizações (Chutes)
* Total de Passes
* Precisão Geral de Passes (%)

### 3. Navegação por Abas (Tabs)

* **📊 Eventos e Métricas:**
  * Utilize o filtro por jogador para isolar o volume de ações de um atleta específico.
  * Visualize contadores individuais de passes e chutes efetuados.

* **🎯 Análise Visual (mplsoccer):**
  * **Mapa de Passes:** Gráfico com vetores de início e fim das jogadas. Passes certos são exibidos em verde e incompletos em vermelho.
  * **Mapa de Chutes (xG):** Visualização no meio-campo ofensivo onde o tamanho do círculo reflete o valor de *Expected Goals* ($xG$) da finalização, e a cor/ícone indica se a jogada resultou em gol.
  * **Heatmap:** Mapa de calor indicando a densidade de ações da partida no gramado.

* **📂 Tabela de Eventos:**
  * Tabela detalhada contendo a cronologia dos eventos da partida.
  * **Botão de Download:** Clique em `📥 Baixar Dados dos Eventos (CSV)` para salvar a tabela filtrada em formato `.csv` no seu computador.

---

## 🛠️ Tecnologias Utilizadas

* [Streamlit](https://streamlit.io/) - Framework de interface gráfica
* [StatsBombPy](https://github.com/statsbomb/statsbombpy) - API/Wrapper de dados abertos da StatsBomb
* [mplsoccer](https://mplsoccer.readthedocs.io/) - Biblioteca especializada no desenho de campos e mapas táticos
* [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) - Visualização de dados
* [Pandas](https://pandas.pydata.org/) - Manipulação e análise de dados