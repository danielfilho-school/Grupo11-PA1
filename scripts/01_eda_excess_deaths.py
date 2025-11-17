#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
01_eda_excess_deaths.py
Análise Exploratória de Dados (AED) – Mortes em Excesso (OMS)

Este script realiza:
- Leitura do dataset da OMS (CSV ou XLSX);
- Padronização de colunas essenciais (country, date, excess, observed, expected);
- Limpeza básica dos dados (datas e numéricos);
- Cálculo de estatísticas globais e por país;
- Geração de gráficos principais:
    • Histograma da distribuição de excess deaths;
    • Série temporal global de excess deaths (mensal);
    • Gráfico de barras dos 15 países com maior excesso acumulado;
    • Gráfico de barras dos 15 países com menor excesso acumulado;
- Exportação de tabelas resumo em CSV.

Uso:
    python 01_eda_excess_deaths.py --input data/excess.csv --out eda_outputs

Parâmetros opcionais:
    --sep       Separador de campos (padrão: ",")
"""

import argparse
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def detect_column(df: pd.DataFrame, options):
    """
    Detecta automaticamente a coluna correta entre diversas opções de nome.
    """
    cols_lower = [c.lower() for c in df.columns]
    for opt in options:
        if opt.lower() in cols_lower:
            return df.columns[cols_lower.index(opt.lower())]
    return None


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza nomes das colunas para:
        country, date, excess, observed, expected
    a partir de possíveis variações presentes no dataset da OMS.

    Lança erro se não conseguir encontrar alguma coluna essencial.
    """
    col_map = {
        "country": detect_column(df, ["country", "location", "entity", "country_name"]),
        "date": detect_column(df, ["date", "month", "time", "year_month", "period"]),
        "excess": detect_column(df, ["excess_deaths", "excess", "excess_deaths_mean"]),
        "observed": detect_column(df, ["observed_deaths", "observed", "deaths"]),
        "expected": detect_column(df, ["expected_deaths", "baseline_deaths", "expected"]),
    }

    missing = [k for k, v in col_map.items() if v is None]
    if missing:
        raise ValueError(
            f"Não foi possível mapear as colunas: {missing}. "
            f"Colunas disponíveis: {list(df.columns)}"
        )

    df = df.rename(columns={
        col_map["country"]: "country",
        col_map["date"]: "date",
        col_map["excess"]: "excess",
        col_map["observed"]: "observed",
        col_map["expected"]: "expected",
    })

    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Caminho para o arquivo CSV/XLSX da OMS.")
    parser.add_argument("--out", required=True, help="Pasta de saída para resultados.")
    parser.add_argument("--sep", default=",", help="Separador (padrão ',').")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    # Leitura do arquivo
    ext = os.path.splitext(args.input)[1].lower()
    if ext in [".xlsx", ".xls"]:
        df = pd.read_excel(args.input)
    else:
        df = pd.read_csv(args.input, sep=args.sep, encoding="utf-8")

    # Padronização de colunas
    df = standardize_columns(df)

    # Conversões de tipo
    df["country"] = df["country"].astype(str).str.strip()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["excess"] = pd.to_numeric(df["excess"], errors="coerce")
    df["observed"] = pd.to_numeric(df["observed"], errors="coerce")
    df["expected"] = pd.to_numeric(df["expected"], errors="coerce")

    # Remove registros sem país ou data
    df = df.dropna(subset=["country", "date"])

    # ---------------------------
    # RESUMO GLOBAL
    # ---------------------------
    summary = {
        "total_rows": len(df),
        "countries": df["country"].nunique(),
        "period_start": df["date"].min().strftime("%Y-%m"),
        "period_end": df["date"].max().strftime("%Y-%m"),
        "missing_excess": int(df["excess"].isna().sum()),
    }
    pd.DataFrame([summary]).to_csv(
        os.path.join(args.out, "overall_summary.csv"), index=False
    )

    # ---------------------------
    # COBERTURA POR PAÍS
    # ---------------------------
    coverage = (
        df.groupby("country")
        .agg(
            start=("date", "min"),
            end=("date", "max"),
            registros=("date", "count"),
            faltantes_excess=("excess", lambda x: int(x.isna().sum())),
        )
        .reset_index()
    )
    coverage.to_csv(os.path.join(args.out, "coverage_by_country.csv"), index=False)

    # ---------------------------
    # RANKING POR PAÍS
    # ---------------------------
    agg = (
        df.groupby("country", as_index=False)
        .agg(total_excess=("excess", "sum"))
        .sort_values("total_excess", ascending=False)
    )
    agg.to_csv(os.path.join(args.out, "agg_by_country.csv"), index=False)

    top15 = agg.head(15)
    bottom15 = agg.tail(15)

    # ---------------------------
    # HISTOGRAMA DE EXCESS DEATHS
    # ---------------------------
    plt.figure()
    df["excess"].dropna().plot(kind="hist", bins=50)
    plt.title("Distribuição do Excesso de Mortes (Todos os Registros)")
    plt.xlabel("Excess deaths")
    plt.ylabel("Frequência")
    plt.tight_layout()
    plt.savefig(os.path.join(args.out, "hist_excess_all.png"))
    plt.close()

    # ---------------------------
    # SÉRIE TEMPORAL GLOBAL (MENSAL)
    # ---------------------------
    ts = (
        df.set_index("date")
        .sort_index()
        .groupby(pd.Grouper(freq="M"))["excess"]
        .sum()
    )

    plt.figure()
    ts.plot()
    plt.title("Excesso de Mortes Global — Série Mensal")
    plt.xlabel("Mês")
    plt.ylabel("Excess deaths (soma mensal)")
    plt.tight_layout()
    plt.savefig(os.path.join(args.out, "timeseries_global_excess.png"))
    plt.close()

    # ---------------------------
    # TOP 15 PAÍSES
    # ---------------------------
    plt.figure()
    plt.bar(top15["country"], top15["total_excess"])
    plt.title("Top 15 Países — Excesso total de mortes")
    plt.xticks(rotation=90)
    plt.ylabel("Excess deaths (soma)")
    plt.tight_layout()
    plt.savefig(os.path.join(args.out, "bar_top15_countries.png"))
    plt.close()

    # ---------------------------
    # BOTTOM 15 PAÍSES
    # ---------------------------
    plt.figure()
    plt.bar(bottom15["country"], bottom15["total_excess"])
    plt.title("Bottom 15 Países — Excesso total de mortes")
    plt.xticks(rotation=90)
    plt.ylabel("Excess deaths (soma)")
    plt.tight_layout()
    plt.savefig(os.path.join(args.out, "bar_bottom15_countries.png"))
    plt.close()

    print("AED concluída com sucesso. Saídas geradas em:", args.out)


if __name__ == "__main__":
    main()
