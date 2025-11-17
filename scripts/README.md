# Scripts de Análise Exploratória (AED)

Esta pasta contém todos os scripts em Python utilizados para a Análise Exploratória de Dados (AED) do dataset de **mortes em excesso associadas à COVID-19**, fornecido pela Organização Mundial da Saúde (OMS).

---

# 🧪 Arquivos

## ▶ 01_eda_excess_deaths.py

Realiza a análise exploratória geral:

- Leitura de CSV/XLSX  
- Padronização automática das colunas  
- Conversões de tipos e limpeza  
- Estatísticas globais  
- Cobertura por país  
- Ranking de países  
- Gráficos:
  - Histograma da distribuição  
  - Série temporal global  
  - Top 15 países  
  - Bottom 15 países

Gera arquivos:
- `hist_excess_all.png`
- `timeseries_global_excess.png`
- `bar_top15_countries.png`
- `bar_bottom15_countries.png`
- `coverage_by_country.csv`
- `agg_by_country.csv`
- `overall_summary.csv`

---

## ▶ 02_eda_country_profiles.py

Gera perfis temporais por país:

- Séries temporais individuais  
- Gráficos `.png` por país  
- Arquivos `summary_{pais}.csv`

Recebe uma lista de países opcional:

--countries "Brazil,India,United States"


---

# 📦 Dependências

Arquivo: `requirements.txt`

pandas>=2.0
numpy>=1.23
matplotlib>=3.8


---

# ▶ Como executar

### AED geral:

python 01_eda_excess_deaths.py --input data/raw/dataset.csv --out outputs/eda


### Perfis por país:

python 02_eda_country_profiles.py --input outputs/eda/arquivo_padronizado.csv --out outputs/perfis --countries "Brazil,India"


---

# 📌 Observações importantes

- Os scripts seguem as boas práticas das **Aulas 01 a 08** de Análise Exploratória.  
- Todos os gráficos utilizam **matplotlib**, conforme exigido.  
- Cada gráfico é salvo em uma figura única (sem subplots).  
- Arquivos CSV gerados são usados para compor o Storytelling da Etapa 3.  

---

# ✔ Estado dos Scripts

100% revisados e funcionando.


