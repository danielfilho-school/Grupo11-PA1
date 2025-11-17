#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
02_eda_country_profiles.py
Perfis temporais de excesso de mortes por país (OMS)

Este script:
- Lê o dataset (já padronizado pelo script 01);
- Gera séries temporais de excess deaths por país;
- Gera arquivos CSV de resumo por país.

Uso:
    python 02_eda_country_profiles.py --input eda_outputs/arquivo_padronizado.csv --out eda_outputs/perfis
    python 02_eda_country_profiles.py --input ... --out ... --countries "Brazil,India,United States"
"""

import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Arquivo CSV de entrada (já padronizado).")
    parser.add_argument("--out", required=True, help="Pasta de saída para gráficos e resumos.")
    parser.add_argument(
        "--countries",
        help="Lista de países separados por vírgula. Ex.: 'Brazil,India,United States'. "
             "Se omitido, gera perfis para todos."
    )
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    df = pd.read_csv(args.input, encoding="utf-8")

    # Checa colunas mínimas
    for col in ["country", "date", "excess"]:
        if col not in df.columns:
            raise ValueError(f"Coluna obrigatória ausente no dataset: {col}")

    # Conversões
    df["country"] = df["country"].astype(str).str.strip()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["excess"] = pd.to_numeric(df["excess"], errors="coerce")

    df = df.dropna(subset=["country", "date"])

    # Lista de países
    if args.countries:
        countries = [c.strip() for c in args.countries.split(",") if c.strip()]
    else:
        countries = sorted(df["country"].unique().tolist())

    for country in countries:
        sub = df[df["country"].str.lower() == country.lower()].copy()

        if sub.empty:
            print(f"Aviso: não há dados para o país: {country}")
            continue

        sub = sub.sort_values("date")

        # Série temporal
        plt.figure()
        plt.plot(sub["date"], sub["excess"])
        plt.title(f"Excesso de Mortes — {country}")
        plt.xlabel("Data")
        plt.ylabel("Excess deaths")
        plt.xticks(rotation=45)
        plt.tight_layout()
        fname_plot = f"timeseries_{country.replace(' ', '_')}.png"
        plt.savefig(os.path.join(args.out, fname_plot))
        plt.close()

        # Resumo numérico
        resumo = {
            "country": country,
            "registros": int(len(sub)),
            "inicio": sub["date"].min().strftime("%Y-%m"),
            "fim": sub["date"].max().strftime("%Y-%m"),
            "excess_sum": float(sub["excess"].sum()),
            "excess_mean": float(sub["excess"].mean()),
            "missing_excess": int(sub["excess"].isna().sum()),
        }

        fname_csv = f"summary_{country.replace(' ', '_')}.csv"
        pd.DataFrame([resumo]).to_csv(
            os.path.join(args.out, fname_csv),
            index=False,
        )

    print("Perfis por país gerados em:", args.out)


if __name__ == "__main__":
    main()

