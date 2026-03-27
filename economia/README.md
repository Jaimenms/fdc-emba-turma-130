# FDC Executive MBA - Turma 130 - Macroeconomics and Microeconomics

## Services for the Mining Sector

![Coverage](coverage.svg)

Data ingestion pipeline for macroeconomics and microeconomics indicators, built as part of the FDC EMBA Turma 130 macroeconomics and microeconomics coursework, with a focus on the Brazilian mining services and engineering sector.

## Data Sources

| Source | Module | Description |
|--------|--------|-------------|
| **SIDRA (IBGE)** | `ingestion/sidra.py` | GDP by sector (extractive, manufacturing, construction), IPCA, IPP, SINAPI, unemployment, industrial production, services, PIA mining, PAIC construction (16 tables) |
| **BCB** | `ingestion/bcb.py` | SELIC rates, USD/BRL exchange rates (PTAX), IGP-M, public debt ratio, trade balance, IBC-Br (8 series) |
| **IPEADATA** | `ingestion/ipeadata.py` | EMBI+ risk, oil prices, steel/iron/laminates production, mineral export indices (quantum/price/FOB), industrial capacity and employment (13 series) |
| **ComexStat (MDIC)** | `ingestion/comexstat.py` | Brazilian trade data via bulk CSVs: monthly totals by SH2 chapter, SH4 product detail (2601=iron ore, 2602=manganese, etc.), and exports by destination country (2010-2026) |
| **World Bank (WDI)** | `ingestion/worldbank.py` | Cross-country comparison (BRA, AUS, CAN, CHL, ZAF, RUS, CHN, USA) for 11 indicators including mineral rents, ore exports share, GFCF |
| **Investing.com** | `ingestion/investpy_minerals.py` | Daily commodity prices: iron ore 62% Fe CFR, gold, copper, silver, aluminum, nickel, zinc, tin, lead, palladium, platinum, coal, steel HRC, uranium (14 commodities) |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[notebooks,dev]"
```

## Usage

```bash
# Ingest all sources
python -m ingestion

# Ingest specific sources (positional or flag)
python -m ingestion sidra,bcb,ipeadata
python -m ingestion --sources comexstat

# List available sources
python -m ingestion --list
```

## Output

All data is written to `data/`, organized in one subfolder per source:

| Path | Content |
|------|---------|
| `sidra/quarterly.csv` | GDP total and by sector (extractive, manufacturing, construction) |
| `sidra/monthly.csv` | IPCA, IPP, SINAPI, unemployment, industrial production, services |
| `sidra/annual.csv` | PIA mining divisions, PAIC construction |
| `bcb/daily.csv` | SELIC (meta + daily), USD/BRL exchange rate (buy + sell) |
| `bcb/monthly.csv` | IGP-M, public debt/GDP, trade balance, IBC-Br |
| `ipeadata/daily.csv` | EMBI+ risk, Brent oil price |
| `ipeadata/monthly.csv` | Steel/iron production, mineral export indices, industrial indicators |
| `comexstat/monthly_totals.csv` | Monthly FOB + kg by SH2 chapter and flow (export/import) |
| `comexstat/monthly_by_sh4.csv` | Monthly detail by 4-digit NCM product code |
| `comexstat/export_ores_by_country.csv` | Chapter 26 ore exports by top 15 destination countries |
| `worldbank/annual.csv` | 11 indicators across 8 countries (1960-2024) |
| `investpy/daily.csv` | 14 mineral commodity closing prices |

Each CSV has a companion `*.dictionary.json` describing its columns (indicator name, source, unit, description).

A consolidated `data/dictionary.json` merges all per-source dictionaries, with a `file` field pointing to each column's CSV.

## Notebooks

Jupyter notebooks with visualizations and analysis for each data source:

| Notebook | Description |
|----------|-------------|
| [bcb.ipynb](notebooks/bcb.ipynb) | SELIC, câmbio USD/BRL, IGP-M, dívida pública, balança comercial, IBC-Br |
| [sidra.ipynb](notebooks/sidra.ipynb) | PIB por setor, IPCA, produção industrial, desemprego, SINAPI, IPP |
| [ipeadata.ipynb](notebooks/ipeadata.ipynb) | EMBI+, petróleo, produção siderúrgica, índices de exportação mineral, indicadores industriais |
| [comexstat.ipynb](notebooks/comexstat.ipynb) | Comércio exterior por capítulo SH2/SH4, minério de ferro por país de destino, preço implícito FOB/ton |
| [worldbank.ipynb](notebooks/worldbank.ipynb) | Comparação internacional: PIB, renda mineral, exportações, investimento (8 países) |
| [investpy.ipynb](notebooks/investpy.ipynb) | Preços diários de commodities minerais: ferro 62% Fe, ouro, cobre, carvão, aço, urânio |

## Configuration

All data source parameters (SIDRA table codes, BCB series IDs, NCM chapters, commodity names, date ranges) are defined in `config.py`.

## Tests

```bash
pytest
pytest --cov=ingestion
```

## References

### SIDRA (IBGE)
- **Portal:** [sidra.ibge.gov.br](https://sidra.ibge.gov.br/)
- **API docs:** [apisidra.ibge.gov.br/home/ajuda](https://apisidra.ibge.gov.br/home/ajuda)
- **Python library:** [sidrapy](https://pypi.org/project/sidrapy/) ([docs](https://sidrapy.readthedocs.io/pt-br/latest/), [GitHub](https://github.com/AlanTaranti/sidrapy))

### BCB (Banco Central do Brasil)
- **SGS - Sistema Gerenciador de Séries Temporais:** [bcb.gov.br/sgs](https://www3.bcb.gov.br/sgspub/)
- **API REST:** `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados?formato=json`
- **API docs:** [dadosabertos.bcb.gov.br](https://dadosabertos.bcb.gov.br/dataset?res_format=API)
- **PTAX (câmbio):** [OLINDA PTAX API](https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/aplicacao#!/recursos)

### IPEADATA
- **Portal:** [ipeadata.gov.br](http://www.ipeadata.gov.br/)
- **API OData4:** `http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{code}')`
- **Metadata:** `http://www.ipeadata.gov.br/api/odata4/Metadados`
- **Data providers:** IMF/IFS (commodities), JP Morgan (EMBI+), IABr (steel/iron production), FUNCEX (trade indices), CNI (industrial indicators)

### ComexStat (MDIC)
- **Portal:** [comexstat.mdic.gov.br](https://comexstat.mdic.gov.br/)
- **Bulk CSV downloads:** `https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/EXP_{year}.csv`
- **Country codes:** `https://balanca.economia.gov.br/balanca/bd/tabelas/PAIS.csv`
- **NCM classification:** [Nomenclatura Comum do Mercosul](https://www.gov.br/siscomex/pt-br/informacoes/nomenclatura-comum-do-mercosul-ncm)
- **ComexVis (interactive):** [comexstat.mdic.gov.br/pt/comex-vis](https://comexstat.mdic.gov.br/pt/comex-vis)

### World Bank (WDI)
- **Data catalog:** [data.worldbank.org](https://data.worldbank.org/)
- **API v2:** `https://api.worldbank.org/v2/country/{codes}/indicator/{indicator}?format=json`
- **API docs:** [datahelpdesk.worldbank.org/knowledgebase/articles/889392](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation)
- **WDI indicators:** [datatopics.worldbank.org/world-development-indicators](https://datatopics.worldbank.org/world-development-indicators/)

### investpy (Investing.com)
- **Python library:** [investpy](https://pypi.org/project/investpy/) ([GitHub](https://github.com/alvarobartt/investpy))
- **Data source:** [investing.com/commodities](https://www.investing.com/commodities/)
- **Standard commodities:** `investpy.commodities.get_commodity_historical_data()` — gold, copper, silver, aluminum, nickel, zinc, tin, lead, palladium, platinum
- **Search-based commodities:** `investpy.search_quotes()` — iron ore 62% Fe CFR (TIOc1/CME), Newcastle coal (ICE), steel HRC FOB China (LME), uranium (CME)

## Project Structure

```
economia/
  config.py              # Source definitions and parameters
  pyproject.toml         # Dependencies and project metadata
  ingestion/
    __init__.py           # CLI entry point and orchestration
    __main__.py           # python -m ingestion runner
    sidra.py              # IBGE SIDRA API
    bcb.py                # Banco Central SGS API
    ipeadata.py           # IPEADATA OData API
    comexstat.py          # MDIC bulk CSV download and processing
    worldbank.py          # World Bank WDI API
    investpy_minerals.py  # Investing.com commodity prices
    dictionary.py         # Per-source and consolidated dictionary builder
  notebooks/              # Jupyter notebooks with visualizations
    bcb.ipynb             # Banco Central indicators
    sidra.ipynb           # IBGE/SIDRA indicators
    ipeadata.ipynb        # IPEADATA indicators
    comexstat.ipynb       # Trade data analysis
    worldbank.ipynb       # International comparison
    investpy.ipynb        # Commodity prices
  tests/                  # Unit tests (mocked API calls)
  data/                   # Generated output (gitignored)
    dictionary.json       # Consolidated data dictionary
    sidra/                # SIDRA CSV + per-file dictionaries
    bcb/                  # BCB CSV + per-file dictionaries
    ipeadata/             # IPEADATA CSV + per-file dictionaries
    comexstat/            # ComexStat CSV + per-file dictionaries
    worldbank/            # World Bank CSV + per-file dictionaries
    investpy/             # investpy CSV + per-file dictionaries
```
