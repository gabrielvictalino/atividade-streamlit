# [IA] Google Antigravity – Métricas e funções de agregação em pandas
"""Métricas (KPIs) e agregações do Dashboard 2.

Funções puras de pandas, sem Streamlit: podem ser importadas no notebook para
validar os números antes de exibi-los no app (slide 15 da Aula 22):

    from src.metricas import calcular_kpis
    calcular_kpis(df)
"""

from dataclasses import dataclass

import pandas as pd

from src.data_loader import COLUNA_CLASSE

CLASSE_ASSISTENCIA = "Gol com Assistência"
PE_ESQUERDO = "Left-footed shot"
MANDANTE = "H"


@dataclass(frozen=True)
class Kpis:
    total_gols: int
    pct_assistencia: float
    minuto_medio: float
    pct_pe_esquerdo: float
    pct_casa: float


def calcular_kpis(df: pd.DataFrame) -> Kpis | None:
    """Calcula os 5 KPIs do recorte. Retorna None se o recorte estiver vazio."""
    if df.empty:
        return None
    return Kpis(
        total_gols=len(df),
        pct_assistencia=float((df[COLUNA_CLASSE] == CLASSE_ASSISTENCIA).mean()),
        minuto_medio=float(df["minuto"].mean()),
        pct_pe_esquerdo=float((df["Type"] == PE_ESQUERDO).mean()),
        pct_casa=float((df["Venue"] == MANDANTE).mean()),
    )


def gols_por_temporada(df: pd.DataFrame) -> pd.DataFrame:
    """Contagem de gols por temporada e classe (formato longo, para barras lado a lado / dodge)."""
    if df.empty:
        return pd.DataFrame(columns=["temporada", COLUNA_CLASSE, "gols"])
    temporadas = sorted(df["temporada"].unique())
    classes = ["Gol com Assistência", "Gol Individual / Sem Assistência"]
    idx = pd.MultiIndex.from_product([temporadas, classes], names=["temporada", COLUNA_CLASSE])
    return (
        df.groupby(["temporada", COLUNA_CLASSE])
        .size()
        .reindex(idx, fill_value=0)
        .reset_index(name="gols")
        .sort_values("temporada")
    )


def gols_por_finalizacao(df: pd.DataFrame) -> pd.DataFrame:
    """Contagem e participação de cada tipo de finalização, do mais ao menos frequente."""
    contagem = df["finalizacao"].value_counts().rename_axis("finalizacao")
    out = contagem.reset_index(name="gols")
    out["participacao"] = out["gols"] / out["gols"].sum()
    return out


def gols_por_adversario(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """Contagem dos principais adversários vitimados no recorte (maiores vítimas)."""
    if df.empty:
        return pd.DataFrame(columns=["adversario", "gols", "participacao"])
    contagem = df["Opponent"].value_counts().head(top_n).rename_axis("adversario")
    out = contagem.reset_index(name="gols")
    total = len(df)
    out["participacao"] = out["gols"] / total if total > 0 else 0
    return out
