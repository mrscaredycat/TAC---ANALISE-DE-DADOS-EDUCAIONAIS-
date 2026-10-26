"""
================================================================================
Etapa 02: Inspeção de Colunas e Variáveis das Bases de Dados (2021 a 2023)
Artigo: Fatores Socioeconômicos e Educacionais e o Desempenho no ENEM (DF)
================================================================================

Este script inspeciona os zips das pastas:
- `2021-2023/2021/`
- `2021-2023/2022 E 2023/`

E lista os metadados e colunas sem precisar extrair gigabytes no disco.
"""

import zipfile
import pandas as pd
from pathlib import Path

ARQUIVOS_CONFIG = {
    2021: {
        "enem_zip": Path("2021-2023/2021/microdados_enem_2021.zip"),
        "enem_csv": "DADOS/MICRODADOS_ENEM_2021.csv",
        "censo_zip": Path("2021-2023/2021/microdados_censo_escolar_2021.zip"),
        "censo_csv": "microdados_ed_basica_2021/dados/microdados_ed_basica_2021.csv"
    },
    2022: {
        "enem_zip": Path("2021-2023/2022 E 2023/microdados_enem_2022.zip"),
        "enem_csv": "DADOS/MICRODADOS_ENEM_2022.csv",
        "censo_zip": Path("2021-2023/2022 E 2023/microdados_censo_escolar_2022.zip"),
        "censo_csv": "Microdados do Censo Escolar da Educaç╞o Básica 2022/dados/microdados_ed_basica_2022.csv"
    },
    2023: {
        "enem_zip": Path("2021-2023/2022 E 2023/microdados_enem_2023.zip"),
        "enem_csv": "microdados_enem_2023/DADOS/MICRODADOS_ENEM_2023.csv",
        "censo_zip": Path("2021-2023/2022 E 2023/microdados_censo_escolar_2023.zip"),
        "censo_csv": "microdados_censo_escolar_2023/dados/microdados_ed_basica_2023.csv"
    }
}

def inspecionar_enem():
    print("=" * 70)
    print("COLUNAS DO ENEM (2021, 2022 e 2023)")
    print("=" * 70)
    for ano, cfg in ARQUIVOS_CONFIG.items():
        if cfg["enem_zip"].exists():
            with zipfile.ZipFile(cfg["enem_zip"], "r") as z:
                with z.open(cfg["enem_csv"]) as f:
                    df = pd.read_csv(f, sep=";", encoding="latin1", nrows=2)
                    print(f"\nAno {ano}: Encontradas {len(df.columns)} colunas.")
        else:
            print(f"Arquivo do ENEM {ano} não encontrado em {cfg['enem_zip']}")

if __name__ == "__main__":
    inspecionar_enem()
