
import pandas as pd
import numpy as np
import statsmodels.api as sm
from pathlib import Path

def executar_regressao():
    caminho_base = Path("data/processed/base_final_modelagem.csv")
    pasta_tabelas = Path("resultados/tabelas")
    pasta_tabelas.mkdir(parents=True, exist_ok=True)
    
    if not caminho_base.exists():
        print(f"Erro: Base {caminho_base} não encontrada.")
        return
        
    df = pd.read_csv(caminho_base, sep=";", encoding="utf-8")
    
    df["ANO_2022"] = (df["NU_ANO"] == 2022).astype(int)
    df["ANO_2023"] = (df["NU_ANO"] == 2023).astype(int)

    variaveis_X = [
        "ESC_PAI_ANOS",
        "ESC_MAE_ANOS",
        "LOG_RENDA",
        "TEM_COMPUTADOR",
        "TEM_INTERNET",
        "ESCOLA_PRIVADA",
        "ESCOLA_FEDERAL",
        "ESCOLA_URBANA",
        "COR_RACA_PPI",
        "SEXO_FEMININO",
        "ANO_2022",
        "ANO_2023"
    ]
    
    df_modelo = df.dropna(subset=["NU_NOTA_MT"] + variaveis_X).copy()
    print(f"Amostra total usada na regressão: {len(df_modelo):,} estudantes do DF.")

    X = df_modelo[variaveis_X]
    X = sm.add_constant(X)
    y = df_modelo["NU_NOTA_MT"]

    modelo = sm.OLS(y, X).fit()
    print("\n" + "=" * 70)
    print("RESUMO DA REGRESSÃO LINEAR MÚLTIPLA (OLS):")
    print("=" * 70)
    print(modelo.summary())

    tabela_coef = pd.DataFrame({
        "Variável": modelo.params.index,
        "Coeficiente (Beta)": modelo.params.values,
        "Erro Padrão": modelo.bse.values,
        "Estatística t": modelo.tvalues.values,
        "p-valor": modelo.pvalues.values,
        "IC_Inferior_95%": modelo.conf_int()[0].values,
        "IC_Superior_95%": modelo.conf_int()[1].values
    })

    mapa_nomes = {
        "const": "Intercepto (Constante)",
        "ESC_PAI_ANOS": "Escolaridade Pai (anos de estudo)",
        "ESC_MAE_ANOS": "Escolaridade Mãe (anos de estudo)",
        "LOG_RENDA": "Renda Familiar Mensal (Log)",
        "TEM_COMPUTADOR": "Possui Computador em Casa (1/0)",
        "TEM_INTERNET": "Possui Internet em Casa (1/0)",
        "ESCOLA_PRIVADA": "Escola Privada (vs Pública Distrital)",
        "ESCOLA_FEDERAL": "Escola Federal (vs Pública Distrital)",
        "ESCOLA_URBANA": "Escola Urbana (vs Rural)",
        "COR_RACA_PPI": "Cor/Raça PPI (Pretos, Pardos, Indígenas)",
        "SEXO_FEMININO": "Sexo Feminino",
        "ANO_2022": "Efeito Ano 2022 (vs 2021)",
        "ANO_2023": "Efeito Ano 2023 (vs 2021)"
    }
    tabela_coef["Nome_Artigo"] = tabela_coef["Variável"].map(mapa_nomes).fillna(tabela_coef["Variável"])
    
    caminho_csv = pasta_tabelas / "regressao_linear_coeficientes.csv"
    tabela_coef.to_csv(caminho_csv, index=False, sep=";", encoding="utf-8")
    
    caminho_txt = pasta_tabelas / "regressao_linear_resumo.txt"
    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write(modelo.summary().as_text())
        f.write(f"\n\nR² do Modelo: {modelo.rsquared:.4f}\n")
        f.write(f"R² Ajustado: {modelo.rsquared_adj:.4f}\n")
        f.write(f"Número de Observações (N): {modelo.nobs}\n")

    print(f"\nTabelas salvas com sucesso em:")
    print(f" - {caminho_csv}")
    print(f" - {caminho_txt}")
    return modelo, tabela_coef

if __name__ == "__main__":
    executar_regressao()
