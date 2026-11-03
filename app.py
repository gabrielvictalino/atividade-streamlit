# [IA] Google Antigravity / Streamlit Skills – Estruturação de layout e componentes do app
import altair as alt
import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import COLUNA_CLASSE, LABELS, VARS_QUANT, load_data
from src.metricas import (
    Kpis,
    calcular_kpis,
    gols_por_adversario,
    gols_por_finalizacao,
    gols_por_temporada,
)

st.set_page_config(
    page_title="Gols de clube de Lionel Messi",
    page_icon=":material/sports_soccer:",
    layout="wide",
)

# Escala divergente Blaugrana/PSG: Azul (#004D98, r = -1) → Neutro (#F4F6F9, 0) → Grená (#A50044, +1)
ESCALA_CORRELACAO = [[0.0, "#004D98"], [0.5, "#F4F6F9"], [1.0, "#A50044"]]
COR_BARRA = "#004D98"
COR_BARRA_SECUNDARIA = "#A50044"
COR_TEXTO_GRAFICO = "#0B1F3A"
CLASSES = {
    "Gol com Assistência": COR_BARRA,
    "Gol Individual / Sem Assistência": COR_BARRA_SECUNDARIA,
}
CHAVE_GRAFICO_TEMPORADAS = "grafico_temporadas"
PARAM_TEMPORADA = "temporada_sel"


def delta_pontos_percentuais(valor: float, referencia: float) -> str | int:
    diferenca = (valor - referencia) * 100
    return 0 if abs(diferenca) < 0.05 else f"{diferenca:+.1f} p.p."


def delta_minutos(valor: float, referencia: float) -> str | int:
    diferenca = valor - referencia
    return 0 if abs(diferenca) < 0.05 else f"{diferenca:+.1f} min"


# [IA] Google Antigravity / Streamlit Skills – Exibição dos 5 cartões de KPI com deltas vs. carreira
def mostrar_kpis(kpis: Kpis, carreira: Kpis) -> None:
    with st.container(horizontal=True):
        st.metric(
            "Gols no recorte",
            f"{kpis.total_gols}",
            delta=f"{kpis.total_gols / carreira.total_gols:.0%} da carreira",
            delta_color="off",
            delta_arrow="off",
            help="Contagem de gols de clube que atendem aos filtros e à temporada selecionada.",
            border=True,
        )
        st.metric(
            "Com assistência",
            f"{kpis.pct_assistencia:.0%}",
            delta=delta_pontos_percentuais(kpis.pct_assistencia, carreira.pct_assistencia),
            delta_color="off",
            delta_description="vs. carreira",
            help="Proporção dos gols que tiveram passe de um companheiro.",
            border=True,
        )
        st.metric(
            "Minuto médio do gol",
            f"{kpis.minuto_medio:.1f}'",
            delta=delta_minutos(kpis.minuto_medio, carreira.minuto_medio),
            delta_color="off",
            delta_description="vs. carreira",
            help="Média do minuto regulamentar do gol (acréscimos contam como 45 ou 90).",
            border=True,
        )
        st.metric(
            "Chute de pé esquerdo",
            f"{kpis.pct_pe_esquerdo:.0%}",
            delta=delta_pontos_percentuais(kpis.pct_pe_esquerdo, carreira.pct_pe_esquerdo),
            delta_color="off",
            delta_description="vs. carreira",
            help="Proporção dos gols marcados com chute de pé esquerdo.",
            border=True,
        )
        st.metric(
            "Gols em casa",
            f"{kpis.pct_casa:.0%}",
            delta=delta_pontos_percentuais(kpis.pct_casa, carreira.pct_casa),
            delta_color="off",
            delta_description="vs. carreira",
            help="Proporção dos gols marcados com o clube como mandante.",
            border=True,
        )


st.title("Gols de clube de Lionel Messi")
st.caption(
    "Cada linha é um gol de clube (FC Barcelona e Paris Saint-Germain, de 2004/05 a "
    "2022/23). A classe da EDA separa gol com assistência de gol individual."
)

df = load_data()

aba_dashboard1, aba_dashboard2 = st.tabs(
    [
        ":material/scatter_plot: Dashboard 1 · Correlação e distribuição",
        ":material/leaderboard: Dashboard 2 · KPIs",
    ],
    on_change="rerun",
)

em_dashboard2 = bool(aba_dashboard2.open)
em_dashboard1 = bool(aba_dashboard1.open) or not em_dashboard2

# [IA] Google Antigravity / Streamlit Skills – Esqueleto da barra lateral e controles de filtro por aba
with st.sidebar:
    if em_dashboard1:
        st.header("Filtros do Dashboard 1")
        st.caption("Selecione as variáveis quantitativas e os intervalos para a análise de correlação e distribuição.")

        variaveis = st.multiselect(
            "Variáveis quantitativas",
            options=VARS_QUANT,
            default=VARS_QUANT,
            format_func=lambda col: LABELS[col],
            help="Selecione as variáveis quantitativas que deseja analisar no dashboard.",
        )

        separar_por_classe = st.toggle(
            "Distinguir por classe",
            value=False,
            help="Colore a distribuição pela classe (participacao_gols: com assistência ou individual).",
        )

        intervalos = {}
        for var in variaveis:
            if pd.api.types.is_integer_dtype(df[var]):
                minimo, maximo, passo = int(df[var].min()), int(df[var].max()), 1
            else:
                minimo, maximo, passo = float(df[var].min()), float(df[var].max()), 0.1
            intervalos[var] = st.slider(
                f"Intervalo de {LABELS[var].lower()}",
                min_value=minimo,
                max_value=maximo,
                value=(minimo, maximo),
                step=passo,
                key=f"intervalo_{var}",
            )
    else:
        st.header("Filtros do Dashboard 2")
        st.caption("Filtre os KPIs e os gráficos de temporada, finalizações e maiores vítimas.")

        clube_opcao = st.selectbox(
            "Clube",
            options=["Todos os clubes", *sorted(df["Club"].unique())],
            index=0,
            key="d2_clube",
            help="Filtra os gols por clube (FC Barcelona, Paris Saint-Germain ou ambos).",
        )

        competicoes = st.multiselect(
            "Competição",
            options=df["Competition"].value_counts().index.tolist(),
            default=[],
            placeholder="Todas as competições",
            key="d2_competicoes",
            help="Selecione uma ou mais competições específicas (vazio = todas).",
        )

        mando_opcao = st.radio(
            "Mando de campo",
            options=["Todos", "Casa (Mandante)", "Fora (Visitante)"],
            index=0,
            key="d2_mando",
            help="Filtra os gols marcados em casa (Home) ou fora (Away).",
        )

        origem_opcao = st.radio(
            "Origem do gol (Classe)",
            options=["Todas", "Gol com Assistência", "Gol Individual / Sem Assistência"],
            index=0,
            key="d2_origem",
            help="Filtra pela variável-alvo da EDA (participacao_gols).",
        )

        min_minuto, max_minuto = int(df["minuto"].min()), int(df["minuto"].max())
        intervalo_minuto_d2 = st.slider(
            "Intervalo de minuto do gol",
            min_value=min_minuto,
            max_value=max_minuto,
            value=(min_minuto, max_minuto),
            step=1,
            key="d2_intervalo_minuto",
        )

# ---------------------------------------------------------------------------
# Dashboard 1: correlação (expandida) + distribuição (gráficos empilhados e todos visíveis)
# [IA] Google Antigravity – Sintaxe Plotly (px.imshow e px.histogram empilhados) e casos de borda
# ---------------------------------------------------------------------------
if em_dashboard1:
    with aba_dashboard1:
        df_filtrado = df
        for var, (inicio, fim) in intervalos.items():
            df_filtrado = df_filtrado[df_filtrado[var].between(inicio, fim)]

        st.caption(f"{len(df_filtrado)} de {len(df)} gols dentro dos intervalos escolhidos.")

        # Seção 1 (Topo, largura total): Mapa de calor da Correlação expandido
        with st.container(border=True):
            st.subheader("Correlação")
            # Variáveis sem variação no recorte (ex.: slider fechado num único valor)
            # geram correlação indefinida, então ficam fora da matriz.
            variaveis_com_variacao = [v for v in variaveis if df_filtrado[v].nunique() > 1]
            variaveis_constantes = [v for v in variaveis if v not in variaveis_com_variacao]

            if len(variaveis) < 2:
                st.info(
                    "Selecione pelo menos 2 variáveis na barra lateral para calcular a correlação.",
                    icon=":material/info:",
                )
            elif len(df_filtrado) < 3:
                st.warning(
                    "Poucos gols no recorte para calcular correlação. Amplie os intervalos.",
                    icon=":material/warning:",
                )
            elif len(variaveis_com_variacao) < 2:
                st.warning(
                    "Menos de 2 variáveis variam dentro dos intervalos atuais. Amplie os intervalos.",
                    icon=":material/warning:",
                )
            else:
                if variaveis_constantes:
                    nomes = ", ".join(LABELS[v].lower() for v in variaveis_constantes)
                    st.caption(f"Fora da matriz por não variar no recorte: {nomes}.")
                matriz = df_filtrado[variaveis_com_variacao].corr()
                rotulos = [LABELS[col] for col in variaveis_com_variacao]
                figura_corr = px.imshow(
                    matriz,
                    x=rotulos,
                    y=rotulos,
                    text_auto=".2f",
                    color_continuous_scale=ESCALA_CORRELACAO,
                    zmin=-1,
                    zmax=1,
                    aspect="auto",
                )
                figura_corr.update_layout(
                    height=520,
                    margin=dict(l=0, r=0, t=24, b=0),
                    coloraxis_colorbar=dict(title="r"),
                )
                figura_corr.update_xaxes(tickangle=0)
                st.plotly_chart(
                    figura_corr,
                    alt="Matriz de correlação de Pearson entre as variáveis quantitativas selecionadas.",
                )

        # Seção 2 (Final da página, largura total): Gráficos de Distribuição empilhados (todos visíveis ao abrir)
        with st.container(border=True):
            st.subheader("Distribuição")
            st.caption(
                "Todos os histogramas das variáveis quantitativas avaliadas ficam visíveis simultaneamente, "
                "empilhados um embaixo do outro."
            )
            if not variaveis:
                st.info(
                    "Selecione pelo menos 1 variável na barra lateral para ver a distribuição.",
                    icon=":material/info:",
                )
            elif df_filtrado.empty:
                st.warning("Nenhum gol restante com os intervalos atuais.", icon=":material/warning:")
            else:
                for var_hist in variaveis:
                    with st.container(border=True):
                        figura_hist = px.histogram(
                            df_filtrado,
                            x=var_hist,
                            color=COLUNA_CLASSE if separar_por_classe else None,
                            color_discrete_map=CLASSES if separar_por_classe else None,
                            color_discrete_sequence=None if separar_por_classe else [COR_BARRA],
                            nbins=20,
                            title=LABELS[var_hist],
                            labels={var_hist: LABELS[var_hist], COLUNA_CLASSE: "Classe"},
                        )
                        figura_hist.update_layout(
                            bargap=0.05,
                            height=270,
                            margin=dict(l=0, r=0, t=36, b=0),
                            xaxis_title=LABELS[var_hist],
                            yaxis_title="Gols",
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, x=1, xanchor="right"),
                        )
                        st.plotly_chart(
                            figura_hist,
                            key=f"hist_{var_hist}",
                            alt=f"Distribuição de {LABELS[var_hist].lower()} nos gols filtrados.",
                        )

# ---------------------------------------------------------------------------
# Dashboard 2: KPIs + gráficos de barra agrupados (dodge e barras horizontais)
# [IA] Google Antigravity / Streamlit Skills – Sintaxe Altair com barras agrupadas (dodge) e seleção cruzada
# ---------------------------------------------------------------------------
if em_dashboard2:
    with aba_dashboard2:
        df_d2 = df.copy()
        if clube_opcao != "Todos os clubes":
            df_d2 = df_d2[df_d2["Club"] == clube_opcao]
        if competicoes:
            df_d2 = df_d2[df_d2["Competition"].isin(competicoes)]
        if mando_opcao == "Casa (Mandante)":
            df_d2 = df_d2[df_d2["Venue"] == "H"]
        elif mando_opcao == "Fora (Visitante)":
            df_d2 = df_d2[df_d2["Venue"] == "A"]
        if origem_opcao != "Todas":
            df_d2 = df_d2[df_d2[COLUNA_CLASSE] == origem_opcao]
        df_d2 = df_d2[df_d2["minuto"].between(intervalo_minuto_d2[0], intervalo_minuto_d2[1])]

        # Seleção cruzada: clicar numa barra de temporada filtra os KPIs e os gráficos abaixo.
        estado_grafico = st.session_state.get(CHAVE_GRAFICO_TEMPORADAS) or {}
        pontos = estado_grafico.get("selection", {}).get(PARAM_TEMPORADA, [])
        temporadas_selecionadas = sorted(
            {p["temporada"] for p in pontos if p.get("temporada") in set(df_d2["temporada"])}
        )
        df_recorte = (
            df_d2[df_d2["temporada"].isin(temporadas_selecionadas)]
            if temporadas_selecionadas
            else df_d2
        )

        kpis = calcular_kpis(df_recorte)
        kpis_carreira = calcular_kpis(df)

        if kpis is None:
            st.warning("Nenhum gol encontrado com a combinação atual de filtros.", icon=":material/warning:")
        else:
            partes_recorte = [
                clube_opcao,
                ", ".join(competicoes) if competicoes else "todas as competições",
                f"mando: {mando_opcao.lower()}" if mando_opcao != "Todos" else "casa e fora",
                f"temporada {', '.join(temporadas_selecionadas)}"
                if temporadas_selecionadas
                else "todas as temporadas",
            ]
            st.caption(
                f"Recorte ativo ({len(df_recorte)} de {len(df)} gols): "
                + " · ".join(partes_recorte)
                + ". Deltas comparam com a carreira inteira."
            )
            mostrar_kpis(kpis, kpis_carreira)

            # Linha 1 (expandida em largura total): Gols por temporada em modo DODGE (lado a lado por classe)
            with st.container(border=True):
                st.subheader("Gols por temporada (com assistência vs. individual)")
                st.caption(
                    "Barras agrupadas lado a lado (dodge) por temporada. "
                    "Clique numa barra para filtrar os KPIs e os gráficos abaixo; clique no fundo para limpar."
                )
                selecao = alt.selection_point(name=PARAM_TEMPORADA, fields=["temporada"])
                dados_temporada = gols_por_temporada(df_d2)
                grafico_temporadas = (
                    alt.Chart(dados_temporada)
                    .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
                    .encode(
                        x=alt.X(
                            "temporada:O",
                            title="Temporada",
                            axis=alt.Axis(labelAngle=0),
                        ),
                        xOffset=alt.XOffset(
                            f"{COLUNA_CLASSE}:N",
                            scale=alt.Scale(domain=list(CLASSES)),
                        ),
                        y=alt.Y("gols:Q", title="Gols"),
                        color=alt.Color(
                            f"{COLUNA_CLASSE}:N",
                            title="Origem do gol",
                            scale=alt.Scale(
                                domain=list(CLASSES.keys()),
                                range=[COR_BARRA, COR_BARRA_SECUNDARIA],
                            ),
                            legend=alt.Legend(orient="top"),
                        ),
                        opacity=alt.condition(selecao, alt.value(1.0), alt.value(0.28)),
                        tooltip=[
                            alt.Tooltip("temporada:O", title="Temporada"),
                            alt.Tooltip(f"{COLUNA_CLASSE}:N", title="Classe"),
                            alt.Tooltip("gols:Q", title="Gols"),
                        ],
                    )
                    .add_params(selecao)
                    .properties(height=360)
                )
                st.altair_chart(
                    grafico_temporadas,
                    on_select="rerun",
                    key=CHAVE_GRAFICO_TEMPORADAS,
                    alt="Gráfico de barras agrupadas lado a lado (dodge) com os gols por temporada, separados entre gols com assistência e gols individuais.",
                )

            # Linha 2 (abaixo de Gols por temporada): Como os gols saíram e Maiores vítimas lado a lado
            col_finalizacoes, col_vitimas = st.columns(2)

            with col_finalizacoes:
                with st.container(border=True, height="stretch"):
                    st.subheader("Como os gols saíram")
                    st.caption("Tipo de finalização no recorte selecionado.")
                    finalizacoes = gols_por_finalizacao(df_recorte)
                    max_fin = max(int(finalizacoes["gols"].max()), 1)
                    barras = (
                        alt.Chart(finalizacoes)
                        .mark_bar(color=COR_BARRA, cornerRadiusEnd=3)
                        .encode(
                            y=alt.Y("finalizacao:N", sort="-x", title=None),
                            x=alt.X(
                                "gols:Q",
                                title="Gols",
                                scale=alt.Scale(domain=[0, max_fin * 1.18]),
                            ),
                            tooltip=[
                                alt.Tooltip("finalizacao:N", title="Finalização"),
                                alt.Tooltip("gols:Q", title="Gols"),
                                alt.Tooltip("participacao:Q", title="Participação", format=".1%"),
                            ],
                        )
                    )
                    rotulos = barras.mark_text(align="left", dx=4, color=COR_TEXTO_GRAFICO).encode(
                        text=alt.Text("participacao:Q", format=".0%")
                    )
                    st.altair_chart(
                        (barras + rotulos).properties(height=360),
                        alt="Gráfico de barras horizontais com a quantidade de gols por tipo de finalização.",
                    )

            with col_vitimas:
                with st.container(border=True, height="stretch"):
                    st.subheader("Maiores vítimas")
                    st.caption("Top 5 adversários que mais sofreram gols no recorte.")
                    vitimas = gols_por_adversario(df_recorte, top_n=5)
                    max_vit = max(int(vitimas["gols"].max()), 1)
                    barras_vitimas = (
                        alt.Chart(vitimas)
                        .mark_bar(color=COR_BARRA_SECUNDARIA, cornerRadiusEnd=3)
                        .encode(
                            y=alt.Y("adversario:N", sort="-x", title=None),
                            x=alt.X(
                                "gols:Q",
                                title="Gols",
                                scale=alt.Scale(domain=[0, max_vit * 1.18]),
                            ),
                            tooltip=[
                                alt.Tooltip("adversario:N", title="Adversário"),
                                alt.Tooltip("gols:Q", title="Gols"),
                                alt.Tooltip("participacao:Q", title="Participação no recorte", format=".1%"),
                            ],
                        )
                    )
                    rotulos_vitimas = barras_vitimas.mark_text(align="left", dx=4, color=COR_TEXTO_GRAFICO).encode(
                        text=alt.Text("gols:Q", format="d")
                    )
                    st.altair_chart(
                        (barras_vitimas + rotulos_vitimas).properties(height=360),
                        alt="Gráfico de barras horizontais com os 5 principais adversários vazados no recorte.",
                    )
