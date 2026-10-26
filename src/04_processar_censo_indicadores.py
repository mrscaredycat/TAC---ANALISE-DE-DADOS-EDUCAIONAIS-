"""
================================================================================
Etapa 04: Processamento do Censo Escolar (2021 a 2023) para o DF
Artigo: Fatores Socioeconômicos e Educacionais e o Desempenho no ENEM (DF)
================================================================================

Objetivo:
1. Ler os microdados do Censo Escolar da Educação Básica (2021, 2022 e 2023) direto dos arquivos .zip.
2. Filtrar apenas as escolas situadas no Distrito Federal (SG_UF == 'DF').
3. Extrair indicadores-chave de infraestrutura:
   - IN_LABORATORIO_CIENCIAS
   - IN_LABORATORIO_INFORMATICA
   - IN_BIBLIOTECA
   - IN_INTERNET
   - IN_BANDA_LARGA
   - IN_DESKTOP_ALUNO / QT_DESKTOP_ALUNO
4. Gerar:
   - A base completa das escolas do DF: `data/processed/censo_escolas_df_2021_2023.csv`
   - O perfil consolidado de infraestrutura por rede (Federal, Distrital, Privada):
     `data/processed/perfil_redes_df_infraestrutura.csv`
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
    for match in Path(".").glob(f"**/{nome_padrao}"):
        if match.is_file():
            return match
    return None

CANDIDATOS_CENSO = {
    2021: [
        "microdados_censo_escolar_2021.zip",
        "data/raw/microdados_censo_escolar_2021.zip",
        "2021-2023/2021/microdados_censo_escolar_2021.zip"
    ],
    2022: [
        "microdados_censo_escolar_2022.zip",
        "data/raw/microdados_censo_escolar_2022.zip",
        "2021-2023/2022 E 2023/microdados_censo_escolar_2022.zip"
    ],
    2023: [
        "microdados_censo_escolar_2023.zip",
        "data/raw/microdados_censo_escolar_2023.zip",
        "2021-2023/2022 E 2023/microdados_censo_escolar_2023.zip"
    ]
}

COLUNAS_CENSO = [
    "NU_ANO_CENSO",
    "CO_ENTIDADE",
    "NO_ENTIDADE",
    "SG_UF",
    "CO_MUNICIPIO",
    "NO_MUNICIPIO",
    "TP_DEPENDENCIA",  # 1: Federal, 2: Distrital, 3: Municipal, 4: Privada
    "TP_LOCALIZACAO",  # 1: Urbana, 2: Rural
    "IN_LABORATORIO_CIENCIAS",
    "IN_LABORATORIO_INFORMATICA",
    "IN_BIBLIOTECA",
    "IN_INTERNET",
    "IN_BANDA_LARGA",
    "IN_DESKTOP_ALUNO",
    "QT_DESKTOP_ALUNO"
]

MAPA_DEPENDENCIA = {
    1: "Federal",
    2: "Pública Distrital",
    3: "Municipal",
    4: "Privada"
}

def processar_censo_ano(ano, candidatos):
    nome_zip = f"microdados_censo_escolar_{ano}.zip"
    zip_path = localizar_zip(nome_zip, candidatos)
    
    if not zip_path:
        print(f"[ALERTA] ZIP do Censo {ano} não encontrado.")
        return None
        
    print(f"\nLendo Censo {ano} a partir de: {zip_path}")
    chunks_df = []
    
    with zipfile.ZipFile(zip_path, "r") as z:
        # Detectar o arquivo de microdados de educação básica dentro do zip
        alvos_csv = [f for f in z.namelist() if f.lower().endswith(f"microdados_ed_basica_{ano}.csv")]
        if not alvos_csv:
            alvos_csv = [f for f in z.namelist() if "microdados_ed_basica" in f.lower() and f.lower().endswith(".csv")]
        if not alvos_csv:
            print(f"[ERRO] Nenhum CSV de microdados do Censo encontrado em {zip_path.name}")
            return None
            
        csv_name = alvos_csv[0]
        print(f"Lendo internamente: {csv_name}")

        with z.open(csv_name) as f:
            for chunk in pd.read_csv(
                f,
                sep=";",
                encoding="latin1",
                usecols=lambda c: c in COLUNAS_CENSO,
                chunksize=50000,
                low_memory=False
            ):
                filtro = chunk["SG_UF"] == "DF"
                sub = chunk[filtro].copy()
                if not sub.empty:
                    if "NU_ANO_CENSO" not in sub.columns:
                        sub["NU_ANO_CENSO"] = ano
                    chunks_df.append(sub)
                    
    if chunks_df:
        df_censo_df = pd.concat(chunks_df, ignore_index=True)
        print(f"Censo {ano}: {len(df_censo_df)} escolas do DF carregadas.")
        return df_censo_df
    return None

def executar_processamento_censo():
    dfs = []
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    
    for ano, candidatos in CANDIDATOS_CENSO.items():
        df_ano = processar_censo_ano(ano, candidatos)
        if df_ano is not None:
            dfs.append(df_ano)
            
    if dfs:
        df_todas = pd.concat(dfs, ignore_index=True)
        caminho_escolas = Path("data/processed/censo_escolas_df_2021_2023.csv")
        df_todas.to_csv(caminho_escolas, sep=";", index=False, encoding="utf-8")
        print(f"\nBase do Censo de Escolas do DF salva em: {caminho_escolas}")
        
        # Gerar perfil de infraestrutura por rede
        df_todas["NOME_REDE"] = df_todas["TP_DEPENDENCIA"].map(MAPA_DEPENDENCIA)
        cols_infra = [
            "IN_LABORATORIO_CIENCIAS",
            "IN_LABORATORIO_INFORMATICA",
            "IN_BIBLIOTECA",
            "IN_INTERNET",
            "IN_BANDA_LARGA",
            "IN_DESKTOP_ALUNO"
        ]
        
        perfil = df_todas.groupby(["NU_ANO_CENSO", "NOME_REDE"])[cols_infra].mean().reset_index()
        caminho_perfil = Path("data/processed/perfil_redes_df_infraestrutura.csv")
        perfil.to_csv(caminho_perfil, sep=";", index=False, encoding="utf-8")
        print(f"Perfil de Infraestrutura por Rede salvo em: {caminho_perfil}")
        print("\nTaxa média de infraestrutura por rede no DF:")
        print(perfil.to_string(index=False))
        return df_todas, perfil

if __name__ == "__main__":
    executar_processamento_censo()
