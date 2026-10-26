"""
================================================================================
Etapa 03: Filtragem e Extração dos Microdados do ENEM (2021 a 2023) para o DF
Artigo: Fatores Socioeconômicos e Educacionais e o Desempenho no ENEM (DF)
================================================================================

Estratégia Otimizada:
1. Lê diretamente dos arquivos .zip de 2021, 2022 e 2023 (sem precisar descompactar).
2. Processa o CSV em streaming com pedaços (chunks) de 100.000 linhas.
3. Filtra apenas os participantes do Distrito Federal (SG_UF_PROVA == 'DF').
4. Mantém apenas quem compareceu à prova de Matemática (TP_PRESENCA_MT == 1 e NU_NOTA_MT não nula).
5. Salva cada ano e o consolidado unificado em `data/processed/enem_df_2021_2023.csv`.
"""

import zipfile
import pandas as pd
from pathlib import Path

# Função auxiliar para localizar o arquivo ZIP em caminhos possíveis
def localizar_zip(nome_padrao, caminhos_candidatos):
    for c in caminhos_candidatos:
        p = Path(c)
        if p.exists():
            return p
    # Busca recursiva se não achou direto
    for match in Path(".").glob(f"**/{nome_padrao}"):
        if match.is_file():
            return match
    return None

CANDIDATOS_ENEM = {
    2021: [
        "microdados_enem_2021.zip",
        "data/raw/microdados_enem_2021.zip",
        "2021-2023/2021/microdados_enem_2021.zip"
    ],
    2022: [
        "microdados_enem_2022.zip",
        "data/raw/microdados_enem_2022.zip",
        "2021-2023/2022 E 2023/microdados_enem_2022.zip"
    ],
    2023: [
        "microdados_enem_2023.zip",
        "data/raw/microdados_enem_2023.zip",
        "2021-2023/2022 E 2023/microdados_enem_2023.zip"
    ]
}

COLUNAS_SELECIONADAS = [
    "NU_INSCRICAO",
    "NU_ANO",
    "TP_FAIXA_ETARIA",
    "TP_SEXO",
    "TP_COR_RACA",
    "SG_UF_PROVA",
    "CO_MUNICIPIO_PROVA",
    "TP_ESCOLA",
    "TP_DEPENDENCIA_ADM_ESC",
    "TP_LOCALIZACAO_ESC",
    "TP_PRESENCA_MT",
    "NU_NOTA_MT",
    "NU_NOTA_CN",
    "NU_NOTA_CH",
    "NU_NOTA_LC",
    "NU_NOTA_REDACAO",
    "Q001",  # Escolaridade Pai
    "Q002",  # Escolaridade Mãe
    "Q006",  # Renda Familiar
    "Q024",  # Computador
    "Q025"   # Internet
]

def filtrar_ano(ano, candidatos, chunksize=100000):
    nome_zip = f"microdados_enem_{ano}.zip"
    zip_path = localizar_zip(nome_zip, candidatos)
    
    if not zip_path:
        print(f"[ALERTA] Arquivo ZIP do ano {ano} não encontrado.")
        return None
        
    print(f"\n" + "=" * 60)
    print(f"Processando ENEM {ano} a partir de: {zip_path}")
    print(f"=" * 60)
    
    chunks_df = []
    total_lidas = 0
    total_df = 0

    with zipfile.ZipFile(zip_path, "r") as z:
        # Detectar o arquivo de microdados dentro do zip
        alvos_csv = [f for f in z.namelist() if f.lower().endswith(f"microdados_enem_{ano}.csv")]
        if not alvos_csv:
            # Fallback para qualquer CSV que contenha MICRODADOS_ENEM
            alvos_csv = [f for f in z.namelist() if "microdados_enem" in f.lower() and f.lower().endswith(".csv")]
        if not alvos_csv:
            print(f"[ERRO] Nenhum CSV de microdados encontrado dentro de {zip_path.name}")
            return None
        
        csv_name = alvos_csv[0]
        print(f"Lendo internamente: {csv_name}")

        with z.open(csv_name) as f:
            for chunk in pd.read_csv(
                f,
                sep=";",
                encoding="latin1",
                usecols=lambda c: c in COLUNAS_SELECIONADAS,
                chunksize=chunksize,
                low_memory=False
            ):
                total_lidas += len(chunk)
                
                # Filtro DF
                filtro = chunk["SG_UF_PROVA"] == "DF"
                sub = chunk[filtro].copy()

                # Filtro Presença e Nota válida em Matemática
                if "TP_PRESENCA_MT" in sub.columns and "NU_NOTA_MT" in sub.columns:
                    sub = sub[(sub["TP_PRESENCA_MT"] == 1) & (sub["NU_NOTA_MT"].notna())]
                
                if not sub.empty:
                    # Garantir coluna do ano
                    if "NU_ANO" not in sub.columns:
                        sub["NU_ANO"] = ano
                    chunks_df.append(sub)
                    total_df += len(sub)
                
                print(f"[{ano}] Linhas lidas: {total_lidas:,} | DF Presentes em MT: {total_df:,}", end="\r")

    print(f"\nFinalizado {ano}! Total retido para o DF: {total_df:,} estudantes.")
    if chunks_df:
        return pd.concat(chunks_df, ignore_index=True)
    return None

def executar_filtragem_completa():
    dfs_anos = []
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    
    for ano, candidatos in CANDIDATOS_ENEM.items():
        df_ano = filtrar_ano(ano, candidatos)
        if df_ano is not None:
            caminho_ano = Path(f"data/processed/enem_df_{ano}.csv")
            df_ano.to_csv(caminho_ano, sep=";", index=False, encoding="utf-8")
            print(f"Salvo: {caminho_ano} ({len(df_ano):,} registros)")
            dfs_anos.append(df_ano)
            
    if dfs_anos:
        df_consolidado = pd.concat(dfs_anos, ignore_index=True)
        caminho_final = Path("data/processed/enem_df_2021_2023.csv")
        df_consolidado.to_csv(caminho_final, sep=";", index=False, encoding="utf-8")
        print("\n" + "=" * 70)
        print(f"SUCESSO: Base consolidada 2021-2023 salva em: {caminho_final}")
        print(f"Total geral de estudantes do DF com nota de MT: {len(df_consolidado):,}")
        print("Distribuição por ano:")
        print(df_consolidado["NU_ANO"].value_counts().sort_index())
        print("=" * 70)
        return df_consolidado

if __name__ == "__main__":
    executar_filtragem_completa()
