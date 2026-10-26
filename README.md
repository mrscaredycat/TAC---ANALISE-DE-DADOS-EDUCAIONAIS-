# Análise de Dados: Fatores Socioeconômicos e o Desempenho no ENEM (DF: 2021–2023)

Trabalho de Conclusão / Artigo Científico:
- **Autores**: Kamily Silva Andrade Crispim, Ana Sarah Nagata, Ana Caroline Freitas Brito
- **Recorte**: Distrito Federal (DF)
- **Período**: 2021 a 2023 (microdados completos e consolidados do Inep)
- **Variável Dependente ($Y$)**: Nota de Matemática (`NU_NOTA_MT`)

---

## 📁 Estrutura de Pastas e Arquivos

```text
analise de dados - TAC/
├── 2021-2023/                         <- Seus arquivos brutos em ZIP (não precisa extrair!)
│   ├── 2021/
│   │   ├── microdados_enem_2021.zip
│   │   └── microdados_censo_escolar_2021.zip
│   └── 2022 E 2023/
│       ├── microdados_enem_2022.zip
│       ├── microdados_enem_2023.zip
│       ├── microdados_censo_escolar_2022.zip
│       └── microdados_censo_escolar_2023.zip
│
├── data/
│   └── processed/                     <- Bases filtradas e tratadas apenas do DF
│       ├── enem_df_2021_2023.csv
│       ├── censo_escolas_df_2021_2023.csv
│       ├── perfil_redes_df_infraestrutura.csv
│       └── base_final_modelagem.csv
│
├── resultados/
│   ├── figuras/                       <- Gráficos em 300 DPI para a Seção 4.1 e 4.3
│   │   ├── heatmap_correlacoes.png
│   │   ├── barras_nota_por_escolaridade_rede.png
│   │   ├── evolucao_desempenho_anos.png
│   │   └── ranking_importancia_variaveis.png
│   └── tabelas/                       <- Tabelas para a Seção 4.2 e 4.3
│       ├── regressao_linear_coeficientes.csv
│       ├── regressao_linear_resumo.txt
│       └── ranking_importancia_random_forest.csv
│
└── src/
    ├── 00_executar_pipeline.py         <- Roda tudo de uma vez
    ├── 01_ambiente_e_verificacao.py    <- Checa ambiente
    ├── 02_inspecionar_colunas.py       <- Mostra metadados e colunas
    ├── 03_filtrar_enem_df.py           <- Filtra ENEM DF por chunks em streaming
    ├── 04_processar_censo_indicadores.py <- Processa Censo Escolar DF
    ├── 05_integrar_bases.py            <- Faz engenharia de atributos e merge
    ├── 06_analise_exploratoria.py      <- Gera Heatmaps e Gráficos
    ├── 07_regressao_linear.py          <- Roda Regressão OLS com estatísticas completas
    └── 08_random_forest.py             <- Treina Random Forest e calcula Feature Importance
```

---

## 🚀 Como Executar

Você pode executar o pipeline inteiro com apenas um comando no terminal:

```powershell
python src/00_executar_pipeline.py
```

Ou executar passo a passo para inspecionar cada etapa:

1. `python src/03_filtrar_enem_df.py`
2. `python src/04_processar_censo_indicadores.py`
3. `python src/05_integrar_bases.py`
4. `python src/06_analise_exploratoria.py`
5. `python src/07_regressao_linear.py`
6. `python src/08_random_forest.py`
