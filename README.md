# FDC Executive MBA - Turma 130

This repository contains relevant information, data, and analyses developed during the **Fundação Dom Cabral (FDC) Executive MBA** program for **Turma 130**.

## Structure

### `economia/`

Data ingestion and analysis pipeline for macroeconomics and microeconomics coursework, with a focus on the Brazilian mining services and engineering sector.

Collects time series from six data sources:

- **SIDRA (IBGE)** — GDP by sector, IPCA, IPP, industrial production, employment, construction costs
- **BCB (Banco Central)** — SELIC, exchange rates (USD/BRL), IGP-M, IBC-Br, trade balance
- **IPEADATA** — EMBI+ risk, steel/iron production, mineral export indices, industrial indicators
- **ComexStat (MDIC)** — Brazilian ore exports/imports by NCM product and destination country
- **World Bank (WDI)** — International comparison across 8 countries (BRA, AUS, CAN, CHL, ZAF, RUS, CHN, USA)
- **investpy (Investing.com)** — Daily mineral commodity prices (iron ore 62% Fe, gold, copper, coal, steel, uranium, and others)

Run the ingestion:

```bash
cd economia
python -m venv .venv && source .venv/bin/activate
pip install -e ".[notebooks,dev]"
python -m ingestion              # all sources
python -m ingestion comexstat    # single source
python -m ingestion --list       # list available sources
```

## About FDC

[Fundação Dom Cabral](https://www.fdc.org.br/) is a Brazilian business school consistently ranked among the top executive education institutions worldwide.
