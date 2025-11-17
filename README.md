\# Projeto Aplicado – Grupo 11  

\## Análise de Mortes em Excesso Associadas à COVID-19 (OMS)



Este repositório contém todas as etapas, scripts, documentos e resultados do Projeto Aplicado do Grupo 11, cujo objetivo é analisar o impacto real da pandemia de COVID-19 por meio do dataset de \*Global Excess Deaths Associated with COVID-19\*, disponibilizado pela Organização Mundial da Saúde (OMS).



---



\# 📊 Objetivo Geral



Realizar uma análise exploratória, analítica e narrativa (storytelling) sobre os dados de \*\*mortes em excesso\*\*, utilizando métodos de Ciência de Dados e técnicas de Data Storytelling, seguindo rigorosamente as etapas estabelecidas no componente curricular.



---



\# 📁 Estrutura do Repositório

├── docs/
│ ├── Etapa1/
│ ├── Etapa2/
│ ├── Etapa3/
│ └── Etapa4/
│
├── data/
│ ├── raw/
│ └── processed/
│
├── scripts/
│ ├── 01_eda_excess_deaths.py
│ ├── 02_eda_country_profiles.py
│ ├── requirements.txt
│ └── README.md
│
├── outputs/
│ ├── eda/
│ └── perfis/
│
└── README.md


---

# 🔍 Dataset Utilizado

**Global Excess Deaths Associated with COVID-19 (Modelled Estimates)**  
Fonte: Organização Mundial da Saúde (OMS/WHO)  
Link: https://www.who.int/data/sets/global-excess-deaths-associated-with-covid-19-modelled-estimates

Tipo de dado: CSV/XLSX, aberto e público.  
Período: 2020–2021  
Escopo: +190 países  

---

# 🧪 Scripts de Análise

Todos os scripts estão na pasta `/scripts/`:

- **01_eda_excess_deaths.py**  
  AED completa do dataset, com gráficos e tabelas agregadas.

- **02_eda_country_profiles.py**  
  Perfis temporais individuais por país.

- **requirements.txt**  
  Dependências (pandas, numpy, matplotlib).

Informações completas de uso estão em `/scripts/README.md`.

---

# 🗂 Resultados

Todos os gráficos e arquivos CSV gerados pelos scripts estão em:

- `/outputs/eda/`  
- `/outputs/perfis/`

---

# 📄 Documentação das Etapas

Toda a documentação formal (PDFs e textos) está em:

/docs/Etapa1
/docs/Etapa2
/docs/Etapa3
/docs/Etapa4


---

# 👨‍💻 Integrantes do Grupo

- Daniel (responsável pela análise, scripts e storytelling)
- Vitor
- [Demais nomes, se houver]

---

# ✔ Como Executar

1. Criar ambiente virtual (opcional):  
   `python -m venv .venv`

2. Ativar ambiente:  
   - Windows: `.venv\Scripts\activate`  
   - Linux/Mac: `source .venv/bin/activate`

3. Instalar dependências:  
   `pip install -r scripts/requirements.txt`

4. Executar AED geral:  
   `python scripts/01_eda_excess_deaths.py --input data/raw/dataset.csv --out outputs/eda`

5. Perfis por país:  
   `python scripts/02_eda_country_profiles.py --input outputs/eda/arquivo.csv --out outputs/perfis`

---

# 📌 Status

**Etapa 1 — OK**  
**Etapa 2 — OK**  
**Etapa 3 — OK**  
**Etapa 4 — Em andamento**

---

# 📚 Licença

Uso exclusivamente acadêmico, conforme diretrizes da OMS.





