"""
================================================================================
Etapa 08: Random Forest Regressor e Feature Importance (Seção 4.3 do Artigo)
Artigo: Fatores Socioeconômicos e Educacionais e o Desempenho no ENEM (DF)
================================================================================

Objetivo:
1. Treinar um modelo não linear (Random Forest Regressor) para predizer NU_NOTA_MT.
2. Dividir a base em 70% Treino e 30% Teste com semente aleatória fixa (random_state=42).
3. Avaliar as métricas de generalização (R², RMSE, MAE) no conjunto de teste.
4. Extrair o Ranking de Importância Relativa das Variáveis (Feature Importance).
5. Gerar o gráfico horizontal para a Seção 4.3 do artigo:
   `resultados/figuras/ranking_importancia_variaveis.png`.
6. Salvar a tabela em `resultados/tabelas/ranking_importancia_random_forest.csv`.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error

def executar_random_forest():
    caminho_base = Path("data/processed/base_final_modelagem.csv")
    pasta_figuras = Path("resultados/figuras")
    pasta_tabelas = Path("resultados/tabelas")
    pasta_figuras.mkdir(parents=True, exist_ok=True)
    pasta_tabelas.mkdir(parents=True, exist_ok=True)
    
    if not caminho_base.exists():
        print(f"Erro: Base {caminho_base} não encontrada.")
        return

    df = pd.read_csv(caminho_base, sep=";", encoding="utf-8")
    
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
        "NU_ANO"
    ]
    
    df_modelo = df.dropna(subset=["NU_NOTA_MT"] + variaveis_X).copy()
    print(f"Total de registros para Random Forest: {len(df_modelo):,}")

    X = df_modelo[variaveis_X]
    y = df_modelo["NU_NOTA_MT"]

    # Divisão 70% Treino e 30% Teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42
    )
    print(f"Tamanho do Treino (70%): {len(X_train):,} | Tamanho do Teste (30%): {len(X_test):,}")

    # Treinamento do Modelo Random Forest
    print("\nTreinando Random Forest Regressor (100 árvores)...")
    rf = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=10,
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)

    # Avaliação no conjunto de Teste
    y_pred = rf.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print("\n" + "=" * 60)
    print("DESEMPENHO PREDITIVO DO MODELO NO TESTE (30%):")
    print("=" * 60)
    print(f"R² Score: {r2:.4f}")
    print(f"RMSE (Raiz do Erro Quadrático Médio): {rmse:.2f} pontos")
    print(f"MAE  (Erro Absoluto Médio):           {mae:.2f} pontos")
    print("=" * 60)

    # Extração de Feature Importance
    mapa_nomes = {
        "ESC_PAI_ANOS": "Escolaridade do Pai",
        "ESC_MAE_ANOS": "Escolaridade da Mãe",
        "LOG_RENDA": "Renda Familiar Mensal",
        "TEM_COMPUTADOR": "Possui Computador em Casa",
        "TEM_INTERNET": "Possui Conexão de Internet",
        "ESCOLA_PRIVADA": "Rede Privada",
        "ESCOLA_FEDERAL": "Rede Federal",
        "ESCOLA_URBANA": "Escola em Área Urbana",
        "COR_RACA_PPI": "Cor/Raça PPI",
        "SEXO_FEMININO": "Sexo Feminino",
        "NU_ANO": "Ano do ENEM"
    }

    importancias = pd.DataFrame({
        "Atributo": [mapa_nomes.get(c, c) for c in variaveis_X],
        "Importancia_Relativa": rf.feature_importances_
    }).sort_values(by="Importancia_Relativa", ascending=False)

    importancias["Percentual"] = (importancias["Importancia_Relativa"] * 100).round(2)
    
    print("\nRANKING DE IMPORTÂNCIA DE VARIÁVEIS (FEATURE IMPORTANCE):")
    print(importancias.to_string(index=False))

    # Salvar Tabela de Importâncias
    caminho_tabela = pasta_tabelas / "ranking_importancia_random_forest.csv"
    importancias.to_csv(caminho_tabela, index=False, sep=";", encoding="utf-8")

    # -------------------------------------------------------------
    # Tabela: Média e Mediana das Notas por Subcategoria (Rubrica UnB)
    # -------------------------------------------------------------
    print("\nCalculando média e mediana de notas de Matemática por subcategoria...")
    linhas_subcategorias = []

    # 1. Rede Escolar
    mapa_rede = {1: "Federal", 2: "Pública Distrital", 4: "Privada"}
    df["Rotulo_Rede"] = df["TP_DEPENDENCIA_ADM_ESC"].map(mapa_rede)
    for subcat, g in df.groupby("Rotulo_Rede")["NU_NOTA_MT"]:
        linhas_subcategorias.append({
            "Dimensao": "Rede de Ensino",
            "Subcategoria": subcat,
            "Total_Estudantes": len(g),
            "Nota_Media": round(g.mean(), 2),
            "Nota_Mediana": round(g.median(), 2),
            "Desvio_Padrao": round(g.std(), 2)
        })

    # 2. Escolaridade Máxima dos Pais
    mapa_rotulos_esc = {
        0: "Sem estudo",
        4: "Fundamental I",
        8: "Fundamental II",
        9: "Fundamental Completo",
        12: "Ensino Médio",
        16: "Ensino Superior",
        18: "Pós-graduação"
    }
    df["Rotulo_Escolaridade"] = df["MAX_ESC_PAIS"].map(mapa_rotulos_esc)
    for subcat, g in df.groupby("Rotulo_Escolaridade")["NU_NOTA_MT"]:
        linhas_subcategorias.append({
            "Dimensao": "Escolaridade Máxima Pais",
            "Subcategoria": subcat,
            "Total_Estudantes": len(g),
            "Nota_Media": round(g.mean(), 2),
            "Nota_Mediana": round(g.median(), 2),
            "Desvio_Padrao": round(g.std(), 2)
        })

    # 3. Posse de Computador
    df["Rotulo_PC"] = df["TEM_COMPUTADOR"].map({1: "Possui Computador", 0: "Não Possui"})
    for subcat, g in df.groupby("Rotulo_PC")["NU_NOTA_MT"]:
        linhas_subcategorias.append({
            "Dimensao": "Recursos Digitais",
            "Subcategoria": subcat,
            "Total_Estudantes": len(g),
            "Nota_Media": round(g.mean(), 2),
            "Nota_Mediana": round(g.median(), 2),
            "Desvio_Padrao": round(g.std(), 2)
        })

    # 4. Localização da Escola
    df["Rotulo_Loc"] = df["TP_LOCALIZACAO_ESC"].map({1: "Urbana", 2: "Rural"})
    for subcat, g in df.dropna(subset=["Rotulo_Loc"]).groupby("Rotulo_Loc")["NU_NOTA_MT"]:
        linhas_subcategorias.append({
            "Dimensao": "Localização da Escola",
            "Subcategoria": subcat,
            "Total_Estudantes": len(g),
            "Nota_Media": round(g.mean(), 2),
            "Nota_Mediana": round(g.median(), 2),
            "Desvio_Padrao": round(g.std(), 2)
        })

    # 5. Cor/Raça
    df["Rotulo_Raca"] = df["COR_RACA_PPI"].map({1: "Pretos/Pardos/Indígenas (PPI)", 0: "Brancos/Amarelos"})
    for subcat, g in df.groupby("Rotulo_Raca")["NU_NOTA_MT"]:
        linhas_subcategorias.append({
            "Dimensao": "Cor / Raça",
            "Subcategoria": subcat,
            "Total_Estudantes": len(g),
            "Nota_Media": round(g.mean(), 2),
            "Nota_Mediana": round(g.median(), 2),
            "Desvio_Padrao": round(g.std(), 2)
        })

    df_subcategorias = pd.DataFrame(linhas_subcategorias)
    caminho_subcat = pasta_tabelas / "medias_notas_por_subcategoria.csv"
    df_subcategorias.to_csv(caminho_subcat, index=False, sep=";", encoding="utf-8")
    print(f"Tabela de médias e medianas por subcategoria salva em: {caminho_subcat}")

    # Gráfico de Barras Horizontal
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=importancias,
        x="Percentual",
        y="Atributo",
        hue="Atributo",
        legend=False,
        palette="Blues_r"
    )
    plt.title("Ranking de Importância das Variáveis no Desempenho em Matemática (DF)", pad=15)
    plt.xlabel("Importância Relativa (%)")
    plt.ylabel("Fator Socioeconômico / Educacional")
    for index, value in enumerate(importancias["Percentual"]):
        plt.text(value + 0.3, index, f"{value:.1f}%", va="center", fontsize=10, weight="bold")
    plt.xlim(0, max(importancias["Percentual"]) * 1.15)
    plt.tight_layout()

    caminho_figura = pasta_figuras / "ranking_importancia_variaveis.png"
    p = Path(caminho_figura).resolve()
    for tentativa in range(3):
        try:
            plt.savefig(str(p), dpi=300)
            plt.close()
            print(f"\nGráfico do ranking salvo em: {p.name}")
            break
        except OSError:
            import time
            time.sleep(0.5)

    return rf, importancias, df_subcategorias

if __name__ == "__main__":
    executar_random_forest()
