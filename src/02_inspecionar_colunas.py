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

def localizar_zip(nome_padrao, caminhos_candidatos):
    for c in caminhos_candidatos:
        p = Path(c)
        if p.exists():
            return p
    for match in Path(".").glob(f"**/{nome_padrao}"):
        if match.is_file():
            return match
    return None

def inspecionar_enem():
    print("=" * 70)
    print("COLUNAS DO ENEM (2021, 2022 e 2023)")
    print("=" * 70)
    for ano in [2021, 2022, 2023]:
        nome_zip = f"microdados_enem_{ano}.zip"
        zip_path = localizar_zip(nome_zip, [nome_zip, f"data/raw/{nome_zip}", f"2021-2023/2021/{nome_zip}", f"2021-2023/2022 E 2023/{nome_zip}"])
        if zip_path and zip_path.exists():
            with zipfile.ZipFile(zip_path, "r") as z:
                alvos = [f for f in z.namelist() if f.lower().endswith(f"microdados_enem_{ano}.csv")]
                if not alvos:
                    alvos = [f for f in z.namelist() if "microdados_enem" in f.lower() and f.lower().endswith(".csv")]
                if alvos:
                    with z.open(alvos[0]) as f:
                        df = pd.read_csv(f, sep=";", encoding="latin1", nrows=2)
                        print(f"\nAno {ano} ({zip_path.name}): {len(df.columns)} colunas identificadas.")
        else:
            print(f"Arquivo do ENEM {ano} não encontrado.")

if __name__ == "__main__":
    inspecionar_enem()
