"""
================================================================================
Etapa 06: Análise Exploratória e Visualizações (Seção 4.1 do Artigo)
Artigo: Fatores Socioeconômicos e Educacionais e o Desempenho no ENEM (DF)
================================================================================

Gera os gráficos científicos em alta resolução (300 DPI) para o artigo:
1. `heatmap_correlacoes.png`: Mapa de calor com coeficientes de correlação linear
   entre nota de Matemática, escolaridade dos pais, renda e infraestrutura.
2. `barras_nota_por_escolaridade_rede.png`: Gráfico de barras agrupadas comparando
   a nota média por nível de escolaridade dos pais entre escolas públicas e privadas.
3. `evolucao_desempenho_anos.png`: Desempenho médio no DF ao longo dos anos 2021 a 2023.
4. `boxplot_renda_nota.png`: Distribuição das notas de matemática por faixas de renda familiar.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configurações estéticas para gráficos padrão publicação científica
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.size": 11,
    "font.family": "sans-serif",
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "figure.titlesize": 14
})

def salvar_figura(caminho, dpi=300):
    import time
    p = Path(caminho).resolve()
    for tentativa in range(3):
        try:
            plt.savefig(str(p), dpi=dpi)
            plt.close()
            print(f"Salvo: {p.name}")
            return
        except OSError:
            time.sleep(0.5)
    plt.savefig(str(p), dpi=dpi)
    plt.close()
    print(f"Salvo: {p.name}")

def gerar_graficos():
    caminho_base = Path("data/processed/base_final_modelagem.csv")
    pasta_figuras = Path("resultados/figuras")
    pasta_figuras.mkdir(parents=True, exist_ok=True)
    
    if not caminho_base.exists():
        print(f"Erro: Base {caminho_base} não encontrada.")
        return
        
    df = pd.read_csv(caminho_base, sep=";", encoding="utf-8")
    print(f"Carregados {len(df):,} registros para análise exploratória.")

    # -------------------------------------------------------------
    # 1. Heatmap de Correlação (Inep + IBGE + Censo Escolar)
    # -------------------------------------------------------------
    print("Gerando Heatmap de correlação...")
    cols_corr = [
        "NU_NOTA_MT",
        "ESC_PAI_ANOS",
        "ESC_MAE_ANOS",
        "LOG_RENDA",
        "PIB_PER_CAPITA",
        "TEM_COMPUTADOR",
        "TEM_INTERNET",
        "ESCOLA_PRIVADA",
        "ESCOLA_URBANA",
        "IN_LABORATORIO_INFORMATICA",
        "IN_BIBLIOTECA",
        "COR_RACA_PPI"
    ]
    cols_existentes = [c for c in cols_corr if c in df.columns]
    corr_matrix = df[cols_existentes].corr()
    
    # Rótulos legíveis em português para o artigo
    rotulos = {
        "NU_NOTA_MT": "Nota Matemática",
        "ESC_PAI_ANOS": "Escolaridade Pai",
        "ESC_MAE_ANOS": "Escolaridade Mãe",
        "LOG_RENDA": "Renda Familiar (Log)",
        "PIB_PER_CAPITA": "PIB per capita DF (IBGE)",
        "TEM_COMPUTADOR": "Tem Computador",
        "TEM_INTERNET": "Tem Internet",
        "ESCOLA_PRIVADA": "Escola Privada",
        "ESCOLA_URBANA": "Escola Urbana",
        "IN_LABORATORIO_INFORMATICA": "Lab. Informática (Escola)",
        "IN_BIBLIOTECA": "Biblioteca (Escola)",
        "COR_RACA_PPI": "PPI (Pretos/Pardos/Ind.)"
    }
    corr_matrix_renamed = corr_matrix.rename(index=rotulos, columns=rotulos)

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr_matrix_renamed,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        vmin=-0.4,
        vmax=0.7,
        linewidths=0.5,
        cbar_kws={"label": "Coeficiente de Correlação de Pearson"}
    )
    plt.title("Matriz de Correlação: Inep (ENEM/Censo) e IBGE (PIB do DF) com Nota de Matemática", pad=15)
    plt.tight_layout()
    caminho_heatmap = pasta_figuras / "heatmap_correlacoes.png"
    salvar_figura(caminho_heatmap)

    # -------------------------------------------------------------
    # 2. Gráfico de Barras Agrupadas: MEDIANA da Nota MT por Escolaridade dos Pais e Rede
    # -------------------------------------------------------------
    print("Gerando Gráfico de Barras Agrupadas (Mediana por Rede)...")
    df_valid = df.dropna(subset=["MAX_ESC_PAIS", "TP_ESCOLA", "NU_NOTA_MT"]).copy()
    df_valid = df_valid[df_valid["TP_ESCOLA"].isin([2, 3])]
    df_valid["Rede"] = df_valid["TP_ESCOLA"].map({2: "Pública", 3: "Privada"})
    
    mapa_rotulos_esc = {
        0: "Sem estudo",
        4: "Fund. I (incompl.)",
        8: "Fund. II (incompl.)",
        9: "Fund. Compl.",
        12: "Médio Compl.",
        16: "Superior Compl.",
        18: "Pós-graduação"
    }
    df_valid["Escolaridade_Rotulo"] = df_valid["MAX_ESC_PAIS"].map(mapa_rotulos_esc)
    ordem_esc = [mapa_rotulos_esc[k] for k in sorted(mapa_rotulos_esc.keys()) if mapa_rotulos_esc[k] in df_valid["Escolaridade_Rotulo"].unique()]

    plt.figure(figsize=(11, 6))
    sns.barplot(
        data=df_valid,
        x="Escolaridade_Rotulo",
        y="NU_NOTA_MT",
        hue="Rede",
        order=ordem_esc,
        palette={"Pública": "#3498db", "Privada": "#e74c3c"},
        estimator=np.median,
        errorbar=None
    )
    plt.title("Mediana da Nota em Matemática por Escolaridade dos Pais e Rede de Ensino (DF)", pad=15)
    plt.xlabel("Maior Nível de Escolaridade dos Pais")
    plt.ylabel("Mediana da Nota em Matemática")
    plt.xticks(rotation=25, ha="right")
    plt.legend(title="Rede de Ensino", frameon=True)
    plt.ylim(350, 750)
    plt.tight_layout()
    caminho_barras = pasta_figuras / "barras_mediana_escolaridade_rede.png"
    salvar_figura(caminho_barras)

    # -------------------------------------------------------------
    # 3. Gráfico de Barras Agrupadas: MEDIANA por Escolaridade e Localização (Urbana vs Rural)
    # -------------------------------------------------------------
    print("Gerando Gráfico de Barras Agrupadas (Mediana por Localização Urbana/Rural)...")
    df_loc = df.dropna(subset=["MAX_ESC_PAIS", "TP_LOCALIZACAO_ESC", "NU_NOTA_MT"]).copy()
    df_loc["Localizacao"] = df_loc["TP_LOCALIZACAO_ESC"].map({1: "Urbana", 2: "Rural"})
    df_loc = df_loc.dropna(subset=["Localizacao"])
    df_loc["Escolaridade_Rotulo"] = df_loc["MAX_ESC_PAIS"].map(mapa_rotulos_esc)

    if not df_loc.empty:
        plt.figure(figsize=(11, 6))
        sns.barplot(
            data=df_loc,
            x="Escolaridade_Rotulo",
            y="NU_NOTA_MT",
            hue="Localizacao",
            order=ordem_esc,
            palette={"Urbana": "#2ecc71", "Rural": "#e67e22"},
            estimator=np.median,
            errorbar=None
        )
        plt.title("Mediana da Nota em Matemática por Escolaridade dos Pais e Localização da Escola (DF)", pad=15)
        plt.xlabel("Maior Nível de Escolaridade dos Pais")
        plt.ylabel("Mediana da Nota em Matemática")
        plt.xticks(rotation=25, ha="right")
        plt.legend(title="Localização", frameon=True)
        plt.ylim(350, 750)
        plt.tight_layout()
        caminho_barras_loc = pasta_figuras / "barras_mediana_escolaridade_localizacao.png"
        salvar_figura(caminho_barras_loc)

    # -------------------------------------------------------------
    # 4. Gráfico de Barras Agrupadas: MEDIANA por Escolaridade e Acesso Digital (Computador/Internet)
    # -------------------------------------------------------------
    print("Gerando Gráfico de Barras Agrupadas (Mediana por Recursos Digitais)...")
    df_dig = df.dropna(subset=["MAX_ESC_PAIS", "TEM_COMPUTADOR", "NU_NOTA_MT"]).copy()
    df_dig["Computador"] = df_dig["TEM_COMPUTADOR"].map({1: "Com Computador", 0: "Sem Computador"})
    df_dig["Escolaridade_Rotulo"] = df_dig["MAX_ESC_PAIS"].map(mapa_rotulos_esc)

    plt.figure(figsize=(11, 6))
    sns.barplot(
        data=df_dig,
        x="Escolaridade_Rotulo",
        y="NU_NOTA_MT",
        hue="Computador",
        order=ordem_esc,
        palette={"Com Computador": "#9b59b6", "Sem Computador": "#95a5a6"},
        estimator=np.median,
        errorbar=None
    )
    plt.title("Mediana da Nota em Matemática por Escolaridade dos Pais e Posse de Computador (DF)", pad=15)
    plt.xlabel("Maior Nível de Escolaridade dos Pais")
    plt.ylabel("Mediana da Nota em Matemática")
    plt.xticks(rotation=25, ha="right")
    plt.legend(title="Recurso Digital", frameon=True)
    plt.ylim(350, 750)
    plt.tight_layout()
    caminho_barras_dig = pasta_figuras / "barras_mediana_escolaridade_computador.png"
    salvar_figura(caminho_barras_dig)

    # -------------------------------------------------------------
    # 5. Evolução Histórica das Médias (2021 a 2023)
    # -------------------------------------------------------------
    print("Gerando Evolução Anual...")
    plt.figure(figsize=(8, 5))
    sns.lineplot(
        data=df[df["TP_ESCOLA"].isin([2, 3])],
        x="NU_ANO",
        y="NU_NOTA_MT",
        hue=df["TP_ESCOLA"].map({2: "Pública", 3: "Privada"}),
        palette={"Pública": "#3498db", "Privada": "#e74c3c"},
        marker="o",
        linewidth=2.5,
        errorbar=("ci", 95)
    )
    plt.title("Evolução da Nota Média em Matemática no DF (2021-2023)", pad=15)
    plt.xlabel("Ano do Exame")
    plt.ylabel("Nota Média em Matemática")
    plt.xticks([2021, 2022, 2023])
    plt.legend(title="Rede", frameon=True)
    plt.tight_layout()
    caminho_evolucao = pasta_figuras / "evolucao_desempenho_anos.png"
    salvar_figura(caminho_evolucao)
    print("\nVisualizações exploratórias concluídas com sucesso!")

if __name__ == "__main__":
    gerar_graficos()
