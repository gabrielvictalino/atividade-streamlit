# [IA] Google Antigravity – Preparação de dados e carga tratada para o Streamlit
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

# Variáveis quantitativas derivadas do data.csv (análogas à lista VARS_QUANT do notebook)
VARS_QUANT = [
    "minuto",
    "gols_clube",
    "gols_adversario",
    "placar_clube",
    "placar_adversario",
]

LABELS = {
    "minuto": "Minuto",
    "gols_clube": "Gols do clube",
    "gols_adversario": "Gols do adversário",
    "placar_clube": "Placar do clube",
    "placar_adversario": "Placar do adversário",
}

COLUNA_CLASSE = "participacao_gols"
# Paleta Blaugrana / PSG: Azul Royal (#004D98) para gols coletivos e Grená (#A50044) para gols individuais
CLASSES = {
    "Gol com Assistência": "#004D98",
    "Gol Individual / Sem Assistência": "#A50044",
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "data.csv"
CLEAN_PATH = PROJECT_ROOT / "data" / "clean" / "dataset.csv"

# O Excel converteu "11/12" e "12/13" em datas no CSV de origem (as datas dos
# jogos confirmam: 2011-2012 e 2012-2013).
TEMPORADAS_CORROMPIDAS = {"11-Dec": "11/12", "Dec-13": "12/13"}

FINALIZACAO_PT = {
    "Left-footed shot": "Chute de pé esquerdo",
    "Right-footed shot": "Chute de pé direito",
    "Penalty": "Pênalti",
    "Direct free kick": "Falta direta",
    "Header": "Cabeceio",
    "Tap-in": "Toque para o gol",
    "Solo run": "Jogada individual",
    "Penalty rebound": "Rebote de pênalti",
    "Deflected shot on goal": "Chute desviado",
    "Counter attack goal": "Contra-ataque",
    "Chest": "Peito",
    "Long distance kick": "Chute de longe",
}


def _minuto_regulamentar(valor) -> float:
    """Remove acréscimos (ex.: '90+1' → 90), como no notebook de EDA."""
    texto = str(valor)
    if texto.replace("+", "").isdigit():
        return int(texto.split("+")[0])
    return np.nan


def _parse_placar(valor) -> tuple[int, int]:
    texto = str(valor).upper().replace("AET", "").replace("PEN", "").strip()
    esquerda, direita = texto.split(":")[:2]
    return int(esquerda.strip()), int(direita.strip())


def _gols_do_clube(casa: int, fora: int, venue: str) -> tuple[int, int]:
    if venue == "H":
        return casa, fora
    return fora, casa


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica o tratamento da EDA e cria as variáveis quantitativas do dashboard."""
    out = df.copy()
    out.columns = [c.strip() for c in out.columns]
    for col in out.select_dtypes(include="object").columns:
        out[col] = out[col].str.strip()

    # Alvo da EDA: gol com assistência vs. jogada individual
    out[COLUNA_CLASSE] = np.where(
        out["Goal_assist"].isna(),
        "Gol Individual / Sem Assistência",
        "Gol com Assistência",
    )

    out["minuto"] = out["Minute"].map(_minuto_regulamentar)

    placar_final = out["Result"].map(_parse_placar)
    placar_momento = out["At_score"].map(_parse_placar)
    out["gols_clube"], out["gols_adversario"] = zip(
        *[_gols_do_clube(c, f, v) for (c, f), v in zip(placar_final, out["Venue"])]
    )
    out["placar_clube"], out["placar_adversario"] = zip(
        *[_gols_do_clube(c, f, v) for (c, f), v in zip(placar_momento, out["Venue"])]
    )

    # Uma linha sem Type; Goal_assist nulo é informativo (gol sem assistência)
    out = out.dropna(subset=["Type", "minuto"]).reset_index(drop=True)

    colunas = [
        "Season",
        "Competition",
        "Matchday",
        "Date",
        "Venue",
        "Club",
        "Opponent",
        "Result",
        "Playing_Position",
        "Minute",
        "At_score",
        "Type",
        "Goal_assist",
        COLUNA_CLASSE,
        *VARS_QUANT,
    ]
    return out[colunas]


def export_clean_dataset(
    raw_path: Path = RAW_PATH, clean_path: Path = CLEAN_PATH
) -> pd.DataFrame:
    raw = pd.read_csv(raw_path)
    clean = prepare_dataframe(raw)
    clean_path.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(clean_path, index=False)
    return clean


def adicionar_colunas_dashboard(df: pd.DataFrame) -> pd.DataFrame:
    """Cria colunas de apresentação usadas no Dashboard 2 (não altera o CSV)."""
    out = df.copy()
    out["temporada"] = out["Season"].replace(TEMPORADAS_CORROMPIDAS)
    out["finalizacao"] = out["Type"].map(FINALIZACAO_PT).fillna(out["Type"])
    return out


@st.cache_data
def load_data(path: str = str(CLEAN_PATH)) -> pd.DataFrame:
    """Lê o dataset já tratado (exportado a partir do notebook de EDA)."""
    return adicionar_colunas_dashboard(pd.read_csv(path))


if __name__ == "__main__":
    df_clean = export_clean_dataset()
    print(f"Exportado {len(df_clean)} linhas x {df_clean.shape[1]} colunas em {CLEAN_PATH}")
