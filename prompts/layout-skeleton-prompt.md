# Template: rascunho de layout → esqueleto do app

Preencha cada bloco e envie à ferramenta de IA.

## Contexto

Sou aluno da disciplina **Análise e Visualização de Dados (AVD 2026.2)** da CESAR School. Estou construindo uma aplicação interativa em **Streamlit** a partir da minha Análise Exploratória de Dados (EDA) sobre os **Gols de Clube de Lionel Messi** (FC Barcelona e Paris Saint-Germain, de 2004/05 a 2022/23, com 703 gols após limpeza). A variável-alvo da EDA é `participacao_gols` ("Gol com Assistência" vs. "Gol Individual / Sem Assistência"), e a identidade visual utiliza a paleta Blaugrana/PSG (`#004D98`, `#A50044`, `#0B1F3A`, `#F8FAFC`).

A aplicação possui dois dashboards divididos em abas (`st.tabs`):
- **Dashboard 1:** Laboratório de correlação e distribuição das variáveis quantitativas (`minuto`, `gols_clube`, `gols_adversario`, `placar_clube`, `placar_adversario`).
- **Dashboard 2:** 5 KPIs e 3 visuais analíticos voltados para comissões técnicas e analistas de desempenho.

## Entrada

- **Rascunho do Dashboard 1:** `prompts/prof_rascunho_dashboard1.png` (e `entregas/rascunho-dashboard1.png`) — barra lateral à esquerda com seletor de variáveis quantitativas, toggle de distinção por classe e sliders de intervalo; área principal dividida em duas colunas: **Correlação (heatmap)** à esquerda e **Distribuição (histogramas em abas)** à direita.
- **Rascunho do Dashboard 2:** `prompts/rascunho_dashboard2.jpg` (e `entregas/rascunho-dashboard2.jpg`) — barra superior de filtros (`st.pills` para Clube e `st.multiselect` para Competição), linha com **5 cartões de KPI** (`st.metric` com borda e deltas em relação à carreira inteira) e **3 gráficos de barras lado a lado** (Gols por temporada com seleção cruzada, Como os gols saíram por tipo de finalização e Top 5 Maiores Vítimas).
- **Colunas do dataset tratado (`data/clean/dataset.csv`):** `Season`, `Competition`, `Matchday`, `Date`, `Venue`, `Club`, `Opponent`, `Result`, `Playing_Position`, `Minute`, `At_score`, `Type`, `Goal_assist`, `participacao_gols`, `minuto`, `gols_clube`, `gols_adversario`, `placar_clube`, `placar_adversario`.

## Restrições

- Utilizar exclusivamente a API atual do **Streamlit** seguindo as diretrizes da skill oficial (`developing-with-streamlit` em `.agents/skills/`).
- Não usar `use_container_width` (depreciado) nem CSS injetado via `unsafe_allow_html`; configurar a identidade visual exclusivamente em `.streamlit/config.toml`.
- Carregar os dados exclusivamente a partir de `src/data_loader.py` com cache `@st.cache_data` e manter os cálculos de KPIs e agregações como funções puras de `pandas` em `src/metricas.py`.
- Tratar casos de borda no Dashboard 1 (0 variáveis selecionadas, 1 variável selecionada, variáveis constantes no intervalo filtrado ou recorte vazio).
- Demarcar os trechos gerados com apoio de IA com `# [IA] <ferramenta> – <finalidade>`.

## Formato de saída

- Um único arquivo `app.py` na raiz do repositório, estruturado de cima para baixo (`st.set_page_config`, cabeçalho, `st.sidebar`, `st.tabs` para Dashboard 1 e Dashboard 2), pronto para execução com `streamlit run app.py`.
