
import pandas as pd
import numpy as np
from pathlib import Path

MAPA_ESCOLARIDADE = {
    "A": 0,
    "B": 4,
    "C": 8,
    "D": 9,
    "E": 12,
    "F": 16,
    "G": 18,
    "H": np.nan
}

MAPA_RENDA_REAIS = {
    "A": 0.0,
    "B": 660.0,
    "C": 1650.0,
    "D": 2475.0,
    "E": 3300.0,
    "F": 4400.0,
    "G": 5500.0,
    "H": 6600.0,
    "I": 7700.0,
    "J": 8800.0,
    "K": 9900.0,
    "L": 11000.0,
    "M": 13200.0,
    "N": 16500.0,
    "O": 19800.0,
    "P": 24000.0,
    "Q": 30000.0
}

def preparar_base_modelagem():
    caminho_enem = Path("data/processed/enem_df_2021_2023.csv")
    caminho_perfil = Path("data/processed/perfil_redes_df_infraestrutura.csv")
    
    if not caminho_enem.exists():
        print(f"Erro: Arquivo {caminho_enem} não encontrado. Execute o script 03 primeiro.")
        return None
        
    print(f"Carregando {caminho_enem}...")
    df = pd.read_csv(caminho_enem, sep=";", encoding="utf-8")
    print(f"Total de registros carregados: {len(df):,}")

    df["ESC_PAI_ANOS"] = df["Q001"].map(MAPA_ESCOLARIDADE)
    df["ESC_MAE_ANOS"] = df["Q002"].map(MAPA_ESCOLARIDADE)
    df["MAX_ESC_PAIS"] = df[["ESC_PAI_ANOS", "ESC_MAE_ANOS"]].max(axis=1)

    df["RENDA_FAMILIAR"] = df["Q006"].map(MAPA_RENDA_REAIS)
    df["LOG_RENDA"] = np.log1p(df["RENDA_FAMILIAR"])

    df["TEM_COMPUTADOR"] = df["Q024"].apply(lambda x: 0 if x == "A" else 1 if pd.notna(x) else np.nan)
    df["TEM_INTERNET"] = df["Q025"].apply(lambda x: 1 if x == "B" else 0 if x == "A" else np.nan)

    df["ESCOLA_PRIVADA"] = (df["TP_DEPENDENCIA_ADM_ESC"] == 4).astype(int)
    df["ESCOLA_PUBLICA_DISTRITAL"] = (df["TP_DEPENDENCIA_ADM_ESC"] == 2).astype(int)
    df["ESCOLA_FEDERAL"] = (df["TP_DEPENDENCIA_ADM_ESC"] == 1).astype(int)
    df["ESCOLA_URBANA"] = (df["TP_LOCALIZACAO_ESC"] == 1).astype(int)

    df["SEXO_FEMININO"] = (df["TP_SEXO"] == "F").astype(int)
    df["COR_RACA_PPI"] = df["TP_COR_RACA"].isin([2, 3, 5]).astype(int)

    MAPA_PIB_DF = {
        2021: 92732.27,
        2022: 116713.39,
        2023: 129790.44
    }
    df["PIB_PER_CAPITA"] = df["NU_ANO"].map(MAPA_PIB_DF)
    df["LOG_PIB_PER_CAPITA"] = np.log(df["PIB_PER_CAPITA"])

    if caminho_perfil.exists():
        perfil = pd.read_csv(caminho_perfil, sep=";", encoding="utf-8")
        mapa_dep = {1: "Federal", 2: "Pública Distrital", 4: "Privada"}
        df["NOME_REDE"] = df["TP_DEPENDENCIA_ADM_ESC"].map(mapa_dep)
        df = df.merge(
            perfil,
            left_on=["NU_ANO", "NOME_REDE"],
            right_on=["NU_ANO_CENSO", "NOME_REDE"],
            how="left"
        )
        print("Indicadores de infraestrutura agregados da escola incorporados com sucesso!")

    caminho_saida = Path("data/processed/base_final_modelagem.csv")
    df.to_csv(caminho_saida, sep=";", index=False, encoding="utf-8")
    print(f"\nBase pronta para modelagem salva em: {caminho_saida}")
    print(f"Total de registros válidos: {len(df):,}")
    return df

if __name__ == "__main__":
    preparar_base_modelagem()
