"""
Configuration for SIDRA and external data ingestion.
Each table entry defines the parameters needed for sidrapy.get_table()
and metadata for the data dictionary.
"""

import os

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data")

# ---------------------------------------------------------------------------
# SIDRA table configurations
# ---------------------------------------------------------------------------
TABLES = {
    # === GDP / National Accounts ===
    "pib": {
        "table_code": "1620",
        "name": "PIB - Série encadeada do índice de volume trimestral",
        "description": "Série encadeada do índice de volume trimestral do PIB (Base: média 1995 = 100)",
        "source": "IBGE - Contas Nacionais Trimestrais",
        "frequency": "quarterly",
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "583",
        "period": "all",
        "classifications": {"11255": "90707"},  # PIB a preços de mercado
        "unit": "Número-índice (base: média 1995 = 100)",
        "calculation": "Índice de volume encadeado trimestral com referência na média de 1995",
    },
    "pib_setorial_variacao": {
        "table_code": "5932",
        "name": "PIB - Taxa de variação por setor",
        "description": "Taxa de variação do PIB trimestral por setores (extrativa, transformação, construção, total, mercado)",
        "source": "IBGE - Contas Nacionais Trimestrais",
        "frequency": "quarterly",
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "6561,6562,6563,6564",
        "period": "all",
        "classifications": {"11255": "90691,90692,90693,90694,90707"},
        "unit": "Percentual (%)",
        "calculation": "Taxas de variação trimestral (interanual, acumulada 4 tri, acumulada no ano, tri/tri anterior)",
    },
    "pib_setorial_corrente": {
        "table_code": "1846",
        "name": "PIB - Valores a preços correntes por setor",
        "description": "PIB trimestral a preços correntes por setores (extrativa, transformação, construção, total)",
        "source": "IBGE - Contas Nacionais Trimestrais",
        "frequency": "quarterly",
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "585",
        "period": "all",
        "classifications": {"11255": "90691,90692,90693,90694,90705,90706,90707"},
        "unit": "Milhões de Reais",
        "calculation": "Valor adicionado bruto a preços correntes por setor econômico",
    },
    "pib_setorial_encadeado": {
        "table_code": "6612",
        "name": "PIB - Valores encadeados a preços de 1995 por setor",
        "description": "PIB trimestral encadeado a preços de 1995 por setores",
        "source": "IBGE - Contas Nacionais Trimestrais",
        "frequency": "quarterly",
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "9318",
        "period": "all",
        "classifications": {"11255": "90691,90692,90693,90694,90707"},
        "unit": "Milhões de Reais (preços de 1995)",
        "calculation": "Valores encadeados a preços de 1995 por setor econômico",
    },
    "contas_economicas": {
        "table_code": "2072",
        "name": "Contas econômicas trimestrais",
        "description": "PIB, RNB, poupança bruta, formação de capital, capacidade de financiamento",
        "source": "IBGE - Contas Nacionais Trimestrais",
        "frequency": "quarterly",
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "all",
        "period": "all",
        "classifications": {},
        "unit": "Milhões de Reais",
        "calculation": "Contas econômicas: PIB, renda, poupança, investimento, capacidade de financiamento",
    },

    # === Prices & Indices ===
    "ipca": {
        "table_code": "7060",
        "name": "IPCA - Variação mensal, acumulada no ano e em 12 meses",
        "description": "Índice Nacional de Preços ao Consumidor Amplo - variações e peso mensal (índice geral)",
        "source": "IBGE - IPCA",
        "frequency": "monthly",
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "63,69,2265,66",
        "period": "all",
        "classifications": {"315": "7169"},  # Geral
        "unit": "Percentual (%)",
        "calculation": "Variação mensal (%), acumulada no ano (%), acumulada em 12 meses (%), peso mensal (%)",
    },
    "ipca_grupos": {
        "table_code": "7063",
        "name": "IPCA por grupos",
        "description": "INPC - Variação mensal por grupos",
        "source": "IBGE - INPC",
        "frequency": "monthly",
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "44,68,2292,45",
        "period": "all",
        "classifications": {"315": "7169,7170,7445,7486,7558,7625,7660,7712,7766,7786"},
        "unit": "Percentual (%)",
        "calculation": "Variação mensal (%), acumulada no ano (%), acumulada em 12 meses (%), peso mensal (%) por grupo",
    },
    "ipp": {
        "table_code": "6903",
        "name": "IPP - Índice de Preços ao Produtor",
        "description": "IPP por setor: Indústria Geral, Extrativas e Transformação (Dez/2018=100)",
        "source": "IBGE - IPP",
        "frequency": "monthly",
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "1396,1395,1394,10008",
        "period": "all",
        "classifications": {"842": "46608,46609,46610"},  # Geral, Extrativas, Transformação
        "unit": "Número-índice (Dez/2018=100) e Percentual (%)",
        "calculation": "Variação mensal (%), acumulada no ano (%), interanual (%) e número-índice (dez/2018=100)",
    },
    "sinapi": {
        "table_code": "2296",
        "name": "SINAPI - Custo da construção civil",
        "description": "Custo médio m², variações percentuais da construção civil (total, material, mão de obra)",
        "source": "IBGE - SINAPI",
        "frequency": "monthly",
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "48,2119,2120,1196,1197,1198",
        "period": "all",
        "classifications": {},
        "unit": "Reais (R$/m²) e Percentual (%)",
        "calculation": "Custo médio por m² (total, material, mão de obra) e variações percentuais (mensal, anual, 12 meses)",
    },

    # === Employment & Income ===
    "desocupacao": {
        "table_code": "6381",
        "name": "Taxa de desocupação",
        "description": "Taxa de desocupação das pessoas de 14 anos ou mais de idade",
        "source": "IBGE - PNAD Contínua mensal",
        "frequency": "monthly",
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "4099",
        "period": "all",
        "classifications": {},
        "unit": "Percentual (%)",
        "calculation": "Razão entre o número de pessoas desocupadas e a força de trabalho (trimestre móvel)",
    },
    "rendimento_medio": {
        "table_code": "6390",
        "name": "Rendimento médio real de todos os trabalhos",
        "description": "Rendimento médio real habitual de todos os trabalhos das pessoas de 14 anos ou mais de idade",
        "source": "IBGE - PNAD Contínua mensal",
        "frequency": "monthly",
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "5933,5929",
        "period": "all",
        "classifications": {},
        "unit": "Reais (R$)",
        "calculation": "Média do rendimento habitualmente recebido de todos os trabalhos (real e nominal), trimestre móvel",
    },

    # === Industrial Production ===
    "producao_fisica_industrial": {
        "table_code": "8888",
        "name": "Produção Física Industrial por seções e atividades",
        "description": "Produção Física Industrial: Geral, Extrativas e Transformação (2022=100)",
        "source": "IBGE - Pesquisa Industrial Mensal - Produção Física",
        "frequency": "monthly",
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "12606,12607,11601,11602,11603,11604",
        "period": "all",
        "classifications": {"544": "129314,129315,129316"},
        "unit": "Número-índice (2022=100) e Percentual (%)",
        "calculation": "Índice de base fixa (2022=100), com ajuste sazonal, e variações percentuais",
    },
    "producao_fisica_grupos": {
        "table_code": "8885",
        "name": "Produção Física Industrial por grupos e classes",
        "description": "Índices de base fixa e variações da produção por grupos e classes industriais (2022=100)",
        "source": "IBGE - Pesquisa Industrial Mensal - Produção Física",
        "frequency": "monthly",
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "12606,11602,11603,11604",
        "period": "all",
        "classifications": {"542": "129176,56681,129180,129195,129199,129200,129204,129207,129210,129212"},
        "unit": "Número-índice (2022=100) e Percentual (%)",
        "calculation": "Índice de base fixa (2022=100) e variações por grupos e classes industriais selecionados",
    },

    # === Services ===
    "servicos_pms": {
        "table_code": "8688",
        "name": "Serviços PMS - Índice de volume de serviços",
        "description": "Índice de volume e receita nominal de serviços por atividades (2022=100)",
        "source": "IBGE - Pesquisa Mensal de Serviços",
        "frequency": "monthly",
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "7167,7168,11623,11624,11625,11626",
        "period": "all",
        "classifications": {
            "11046": "56726",
            "12355": "107071",
        },
        "unit": "Número-índice (2022=100) e Percentual (%)",
        "calculation": "Índice de volume de serviços (2022=100), com ajuste sazonal, e variações percentuais",
    },

    # === Annual Structural Surveys (Mining & Construction) ===
    "pia_mineracao": {
        "table_code": "5548",
        "name": "PIA - Dados da indústria extrativa por divisão CNAE",
        "description": "Dados anuais de empresas industriais: carvão, petróleo, minerais metálicos, não-metálicos, apoio à mineração",
        "source": "IBGE - Pesquisa Industrial Anual - Empresa",
        "frequency": "annual",
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "630,631,802,803,805",
        "period": "all",
        "classifications": {"12762": "116881,116884,116887,116897,116905"},
        "unit": "Unidades, Pessoas, Mil Reais",
        "calculation": "Número de empresas, pessoal ocupado, custos/despesas totais, despesas com pessoal, receita bruta",
    },
    "paic_construcao": {
        "table_code": "1739",
        "name": "PAIC - Indústria da construção por atividade",
        "description": "Dados anuais da construção: edificações, infraestrutura, serviços especializados",
        "source": "IBGE - Pesquisa Anual da Indústria da Construção",
        "frequency": "annual",
        "territorial_level": "1",
        "ibge_territorial_code": "all",
        "variable": "630,631,1239,1242",
        "period": "all",
        "classifications": {},
        "unit": "Unidades, Pessoas, Mil Reais",
        "calculation": "Número de empresas, pessoal ocupado, receita bruta, valor adicionado",
    },
    # PAS table 2634 excluded — returns suppressed data ("..") at national aggregate level
}

# ---------------------------------------------------------------------------
# BCB (Banco Central do Brasil) - SGS series
# ---------------------------------------------------------------------------
BCB_SERIES = {
    "selic_meta": {
        "code": 432,
        "name": "Taxa SELIC - Meta",
        "description": "Taxa básica de juros definida pelo COPOM",
        "source": "Banco Central do Brasil",
        "frequency": "daily",
        "unit": "% a.a.",
    },
    "selic_diaria": {
        "code": 11,
        "name": "Taxa SELIC - Diária",
        "description": "Taxa SELIC efetiva diária (anualizada)",
        "source": "Banco Central do Brasil",
        "frequency": "daily",
        "unit": "% a.a.",
    },
    "cambio_venda": {
        "code": 1,
        "name": "Câmbio USD/BRL - Venda",
        "description": "Taxa de câmbio comercial dólar americano (venda)",
        "source": "Banco Central do Brasil",
        "frequency": "daily",
        "unit": "BRL/USD",
    },
    "cambio_compra": {
        "code": 10813,
        "name": "Câmbio USD/BRL - Compra",
        "description": "Taxa de câmbio comercial dólar americano (compra)",
        "source": "Banco Central do Brasil",
        "frequency": "daily",
        "unit": "BRL/USD",
    },
    "igpm": {
        "code": 189,
        "name": "IGP-M - Variação mensal",
        "description": "Índice Geral de Preços - Mercado (variação % mensal)",
        "source": "FGV via Banco Central do Brasil",
        "frequency": "monthly",
        "unit": "% mensal",
    },
    "divida_liquida_pib": {
        "code": 4513,
        "name": "Dívida líquida do setor público (% PIB)",
        "description": "Dívida líquida do setor público consolidado como proporção do PIB",
        "source": "Banco Central do Brasil",
        "frequency": "monthly",
        "unit": "% do PIB",
    },
    "balanca_comercial": {
        "code": 22707,
        "name": "Balança comercial - Saldo mensal",
        "description": "Saldo da balança comercial (exportações - importações)",
        "source": "Banco Central do Brasil",
        "frequency": "monthly",
        "unit": "US$ milhões",
    },
    "ibc_br": {
        "code": 24364,
        "name": "IBC-Br - Índice de Atividade Econômica",
        "description": "Proxy mensal do PIB calculado pelo Banco Central",
        "source": "Banco Central do Brasil",
        "frequency": "monthly",
        "unit": "Número-índice (2002=100, dessaz.)",
    },
}

# ---------------------------------------------------------------------------
# IPEADATA series (EMBI+, commodity prices)
# ---------------------------------------------------------------------------
IPEADATA_SERIES = {
    "embi_brasil": {
        "code": "JPM366_EMBI366",
        "name": "EMBI+ Brasil (Risco-País)",
        "description": "Emerging Markets Bond Index Plus para o Brasil",
        "source": "JP Morgan via IPEADATA",
        "frequency": "daily",
        "unit": "Pontos-base",
    },
    "preco_petroleo_brent": {
        "code": "EIA366_PBRENT366",
        "name": "Preço do petróleo Brent",
        "description": "Crude oil, Brent, spot price (FOB)",
        "source": "EIA via IPEADATA",
        "frequency": "daily",
        "unit": "US$/barril",
    },
    "preco_petroleo_mensal": {
        "code": "IFS12_PETROLEUM12",
        "name": "Preço do petróleo (cotação internacional, mensal)",
        "description": "Commodities - petróleo - cotação internacional",
        "source": "IMF/IFS via IPEADATA",
        "frequency": "monthly",
        "unit": "US$/barril",
    },
    "producao_aco_bruto": {
        "code": "IBSIE12_QSCAB12",
        "name": "Produção de aço bruto",
        "description": "Transformação mineral - aço bruto - produção mensal",
        "source": "IABr via IPEADATA",
        "frequency": "monthly",
        "unit": "Mil toneladas",
    },
    "producao_ferro_gusa": {
        "code": "IBSIE12_QSCFG12",
        "name": "Produção de ferro-gusa",
        "description": "Transformação mineral - ferro-gusa - produção mensal",
        "source": "IABr via IPEADATA",
        "frequency": "monthly",
        "unit": "Mil toneladas",
    },
    "producao_laminados": {
        "code": "IBSIE12_QSCL12",
        "name": "Produção de laminados",
        "description": "Transformação mineral - laminados - produção mensal",
        "source": "IABr via IPEADATA",
        "frequency": "monthly",
        "unit": "Mil toneladas",
    },
    "export_minerais_metalicos_fob": {
        "code": "FUNCEX_XVEMM2N",
        "name": "Exportações - Minerais metálicos (FOB)",
        "description": "Exportações brasileiras de extração de minerais metálicos (FOB)",
        "source": "FUNCEX via IPEADATA",
        "frequency": "monthly",
        "unit": "US$ milhões",
    },
    "export_minerais_metalicos_quantum": {
        "code": "FUNCEX12_XQEMM2N12",
        "name": "Exportações - Minerais metálicos (quantum)",
        "description": "Exportações - extração de minerais metálicos - índice de quantum (média 2018=100)",
        "source": "FUNCEX via IPEADATA",
        "frequency": "monthly",
        "unit": "Índice (média 2018=100)",
    },
    "export_minerais_metalicos_preco": {
        "code": "FUNCEX12_XPEMM2N12",
        "name": "Exportações - Minerais metálicos (preço)",
        "description": "Exportações - extração de minerais metálicos - índice de preços (média 2018=100)",
        "source": "FUNCEX via IPEADATA",
        "frequency": "monthly",
        "unit": "Índice (média 2018=100)",
    },
    "export_metalurgia_fob": {
        "code": "FUNCEX12_XVMETBAS2N12",
        "name": "Exportações - Metalurgia (FOB)",
        "description": "Exportações brasileiras de metalurgia (FOB)",
        "source": "FUNCEX via IPEADATA",
        "frequency": "monthly",
        "unit": "US$ milhões",
    },
    "utilizacao_capacidade_industrial": {
        "code": "CNI12_NUCAP12",
        "name": "Utilização da capacidade instalada - Indústria",
        "description": "Indicadores Industriais CNI - utilização da capacidade instalada (média 2006=100)",
        "source": "CNI via IPEADATA",
        "frequency": "monthly",
        "unit": "Índice (média 2006=100)",
    },
    "emprego_industrial": {
        "code": "CNI12_PEEMP12",
        "name": "Pessoal empregado - Indústria",
        "description": "Indicadores Industriais CNI - pessoal empregado na indústria (média 2006=100)",
        "source": "CNI via IPEADATA",
        "frequency": "monthly",
        "unit": "Índice (média 2006=100)",
    },
    "faturamento_real_industrial": {
        "code": "CNI12_VENREA12",
        "name": "Faturamento real - Indústria",
        "description": "Indicadores Industriais CNI - faturamento real da indústria (média 2006=100)",
        "source": "CNI via IPEADATA",
        "frequency": "monthly",
        "unit": "Índice (média 2006=100)",
    },
}

# ---------------------------------------------------------------------------
# ComexStat - Brazilian trade data (exports/imports) via MDIC bulk CSVs
# SH2 chapters: 26=Ores, 27=Fuels, 72=Iron/Steel, 84=Machinery
# SH4 detail for ores: 2601=Iron ore, 2602=Manganese, 2603=Copper, etc.
# ---------------------------------------------------------------------------
COMEXSTAT_YEARS = list(range(2010, 2027))

COMEXSTAT_ORE_PRODUCTS = {
    "ores_minerals": {
        "sh2_codes": ["26"],
        "name": "Minérios, escórias e cinzas (cap. 26)",
        "description": "Iron ore (2601), manganese (2602), copper (2603), nickel (2604), "
                       "cobalt (2605), aluminum/bauxite (2606), lead (2607), zinc (2608), "
                       "tin (2609), chromium (2610), tungsten (2611), uranium (2612), "
                       "titanium (2614), niobium (2615), precious metals ores (2616), "
                       "other ores (2617), slag/ash (2620-2621)",
    },
    "iron_steel": {
        "sh2_codes": ["72"],
        "name": "Ferro fundido, ferro e aço (cap. 72)",
        "description": "Pig iron, steel, ferro-alloys, flat/long products",
    },
    "fuels": {
        "sh2_codes": ["27"],
        "name": "Combustíveis minerais (cap. 27)",
        "description": "Petroleum, coal, natural gas and derivatives",
    },
    "machinery": {
        "sh2_codes": ["84"],
        "name": "Máquinas e equipamentos mecânicos (cap. 84)",
        "description": "Machinery, mechanical equipment, mining/construction equipment",
    },
}

# ---------------------------------------------------------------------------
# World Bank - WDI indicators for international comparison
# Countries: BRA, AUS, CAN, CHL, ZAF, RUS, CHN, USA, WLD
# ---------------------------------------------------------------------------
WORLDBANK_INDICATORS = {
    "industry_gdp_pct": {
        "code": "NV.IND.TOTL.ZS",
        "name": "Industry (incl. construction), value added (% of GDP)",
        "description": "Share of industry (including mining, manufacturing, construction) in GDP",
    },
    "mining_rents_pct_gdp": {
        "code": "NY.GDP.MINR.RT.ZS",
        "name": "Mineral rents (% of GDP)",
        "description": "Difference between value of mineral production and total costs of production",
    },
    "gdp_growth": {
        "code": "NY.GDP.MKTP.KD.ZG",
        "name": "GDP growth (annual %)",
        "description": "Annual percentage growth rate of GDP at constant prices",
    },
    "gdp_per_capita": {
        "code": "NY.GDP.PCAP.CD",
        "name": "GDP per capita (current US$)",
        "description": "Gross domestic product divided by midyear population",
    },
    "exports_goods_services_pct_gdp": {
        "code": "NE.EXP.GNFS.ZS",
        "name": "Exports of goods and services (% of GDP)",
        "description": "Value of all goods and services exported as share of GDP",
    },
    "ore_metals_exports_pct": {
        "code": "TX.VAL.MMTL.ZS.UN",
        "name": "Ores and metals exports (% of merchandise exports)",
        "description": "Share of ores and metals in total merchandise exports",
    },
    "fuel_exports_pct": {
        "code": "TX.VAL.FUEL.ZS.UN",
        "name": "Fuel exports (% of merchandise exports)",
        "description": "Share of fuel in total merchandise exports",
    },
    "gfcf_pct_gdp": {
        "code": "NE.GDI.FTOT.ZS",
        "name": "Gross fixed capital formation (% of GDP)",
        "description": "Investment in fixed assets as share of GDP (proxy for engineering/construction intensity)",
    },
    "inflation_cpi": {
        "code": "FP.CPI.TOTL.ZG",
        "name": "Inflation, consumer prices (annual %)",
        "description": "Annual percentage change in consumer price index",
    },
    "unemployment": {
        "code": "SL.UEM.TOTL.ZS",
        "name": "Unemployment, total (% of labor force)",
        "description": "Share of labor force that is without work but seeking employment",
    },
    "total_natural_resources_rents": {
        "code": "NY.GDP.TOTL.RT.ZS",
        "name": "Total natural resources rents (% of GDP)",
        "description": "Sum of oil, gas, coal, mineral, and forest rents",
    },
}

WORLDBANK_COUNTRIES = "BRA;AUS;CAN;CHL;ZAF;RUS;CHN;USA"

# ---------------------------------------------------------------------------
# investpy - Mineral commodity prices from Investing.com
# ---------------------------------------------------------------------------
INVESTPY_COMMODITIES = {
    "gold": {
        "commodity": "Gold",
        "name": "Ouro (Gold)",
        "description": "Gold futures price, COMEX",
        "source": "Investing.com via investpy",
        "unit": "US$/troy oz",
        "from_date": "01/01/2000",
        "to_date": "27/03/2026",
    },
    "copper": {
        "commodity": "Copper",
        "name": "Cobre (Copper)",
        "description": "Copper futures price, COMEX",
        "source": "Investing.com via investpy",
        "unit": "US$/lb",
        "from_date": "01/01/2000",
        "to_date": "27/03/2026",
    },
    "silver": {
        "commodity": "Silver",
        "name": "Prata (Silver)",
        "description": "Silver futures price, COMEX",
        "source": "Investing.com via investpy",
        "unit": "US$/troy oz",
        "from_date": "01/01/2000",
        "to_date": "27/03/2026",
    },
    "aluminum": {
        "commodity": "Aluminum",
        "name": "Alumínio (Aluminum)",
        "description": "Aluminum futures price, LME",
        "source": "Investing.com via investpy",
        "unit": "US$/ton",
        "from_date": "01/01/2000",
        "to_date": "27/03/2026",
    },
    "nickel": {
        "commodity": "Nickel",
        "name": "Níquel (Nickel)",
        "description": "Nickel futures price, LME",
        "source": "Investing.com via investpy",
        "unit": "US$/ton",
        "from_date": "01/01/2000",
        "to_date": "27/03/2026",
    },
    "zinc": {
        "commodity": "Zinc",
        "name": "Zinco (Zinc)",
        "description": "Zinc futures price, LME",
        "source": "Investing.com via investpy",
        "unit": "US$/ton",
        "from_date": "01/01/2000",
        "to_date": "27/03/2026",
    },
    "tin": {
        "commodity": "Tin",
        "name": "Estanho (Tin)",
        "description": "Tin futures price, LME",
        "source": "Investing.com via investpy",
        "unit": "US$/ton",
        "from_date": "01/01/2000",
        "to_date": "27/03/2026",
    },
    "lead": {
        "commodity": "Lead",
        "name": "Chumbo (Lead)",
        "description": "Lead futures price, LME",
        "source": "Investing.com via investpy",
        "unit": "US$/ton",
        "from_date": "01/01/2000",
        "to_date": "27/03/2026",
    },
    "palladium": {
        "commodity": "Palladium",
        "name": "Paládio (Palladium)",
        "description": "Palladium futures price, NYMEX",
        "source": "Investing.com via investpy",
        "unit": "US$/troy oz",
        "from_date": "01/01/2000",
        "to_date": "27/03/2026",
    },
    "platinum": {
        "commodity": "Platinum",
        "name": "Platina (Platinum)",
        "description": "Platinum futures price, NYMEX",
        "source": "Investing.com via investpy",
        "unit": "US$/troy oz",
        "from_date": "01/01/2000",
        "to_date": "27/03/2026",
    },

    # --- Fetched via search_quotes (not in standard investpy commodity list) ---

    "iron_ore_62fe": {
        "search_term": "iron ore",
        "name": "Minério de ferro finos 62% Fe CFR",
        "description": "Iron ore fines 62% Fe CFR Futures (TIOc1, CME/SGX)",
        "source": "Investing.com via investpy (search)",
        "unit": "US$/ton",
        "from_date": "01/01/2010",
        "to_date": "27/03/2026",
    },
    "coal_newcastle": {
        "search_term": "coal",
        "name": "Carvão Newcastle Futures",
        "description": "Newcastle Coal Futures (ICE) - benchmark for thermal coal in Asia-Pacific",
        "source": "Investing.com via investpy (search)",
        "unit": "US$/ton",
        "from_date": "01/01/2010",
        "to_date": "27/03/2026",
    },
    "steel_hrc_china": {
        "search_term": "steel",
        "name": "Aço HRC FOB China Futures",
        "description": "Steel HRC (Hot-Rolled Coil) FOB China Futures (LME)",
        "source": "Investing.com via investpy (search)",
        "unit": "US$/ton",
        "from_date": "01/01/2010",
        "to_date": "27/03/2026",
    },
    "uranium": {
        "search_term": "uranium",
        "name": "Urânio Futures",
        "description": "Uranium Futures (CME/UxC)",
        "source": "Investing.com via investpy (search)",
        "unit": "US$/lb",
        "from_date": "01/01/2010",
        "to_date": "27/03/2026",
    },
    "lithium_lit": {
        "search_term": "Global X Lithium",
        "search_product": "etfs",
        "name": "Global X Lithium & Battery Tech ETF (LIT)",
        "description": "LIT ETF — proxy for lithium prices, tracks lithium miners and battery producers (NYSE)",
        "source": "Investing.com via investpy (search)",
        "unit": "US$",
        "from_date": "01/01/2010",
        "to_date": "29/03/2026",
    },
}
