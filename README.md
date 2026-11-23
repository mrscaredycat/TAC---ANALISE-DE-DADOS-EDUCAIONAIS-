# Análise de Dados Educacionais: desempenho em Matemática no ENEM (DF, 2021-2023)

Projeto da disciplina de Tópicos Avançados em Computadores (TAC) — Universidade de Brasília (UnB), Departamento de Ciência da Computação (CIC).

O trabalho analisa como fatores socioeconômicos e educacionais (escolaridade dos pais, renda, rede de ensino, localização e posse de computador) se associam à nota de Matemática dos estudantes do Distrito Federal no ENEM entre 2021 e 2023. A análise usa estatística descritiva, regressão linear múltipla (OLS) e Random Forest. A amostra final tem 126.874 estudantes.

## Equipe

- Ana Caroline Freitas Brito
- Ana Sarah Nagata
- Kamily Silva Andrade Crispim

## Requisitos

- Python 3.10 ou superior
- Dependências listadas em `requirements.txt` (pandas, numpy, scikit-learn, statsmodels, matplotlib, seaborn)

## Como rodar

O repositório já inclui a base tratada em `data/processed/base_final_modelagem.csv`, então é possível reproduzir as análises sem baixar os microdados brutos do Inep.

1. Clonar o repositório:

```bash
git clone https://github.com/mrscaredycat/ANALISE-DE-DADOS-EDUCACIONAIS---TAC.git
cd ANALISE-DE-DADOS-EDUCACIONAIS---TAC
```

2. Instalar as dependências:

```bash
pip install -r requirements.txt
```

3. Rodar o pipeline completo:

```bash
python src/00_executar_pipeline.py
```

Esse comando usa a base já processada e executa, em sequência:

1. `06_analise_exploratoria.py` — gera o mapa de correlação e os gráficos de barras em `resultados/figuras/`;
2. `07_regressao_linear.py` — ajusta a regressão linear (OLS) e salva os coeficientes em `resultados/tabelas/`;
3. `08_random_forest.py` — treina o Random Forest e salva o ranking de importância e as estatísticas por subgrupo.

Para rodar uma etapa isolada, basta chamar o script correspondente, por exemplo:

```bash
python src/07_regressao_linear.py
```

Para reprocessar os microdados brutos do zero, coloque os arquivos `.zip` do Inep/IBGE na raiz do projeto e rode:

```bash
python src/00_executar_pipeline.py --full
```

## Estrutura do projeto

```
ARTIGO.pdf            Artigo final em PDF
requirements.txt      Dependências do projeto
README.md             Este arquivo

data/processed/       Bases já tratadas e integradas (DF, 2021-2023)
                      base_final_modelagem.csv é a base usada nos modelos

resultados/
  figuras/            Gráficos gerados pelos scripts
  tabelas/            Tabelas e resumos estatísticos (CSV e TXT)

src/
  00_executar_pipeline.py        Executa o pipeline completo
  01_ambiente_e_verificacao.py   Verifica dependências
  02_inspecionar_colunas.py      Inspeciona colunas dos microdados
  03_filtrar_enem_df.py          Filtra os microdados do ENEM para o DF
  04_processar_censo_indicadores.py  Processa o Censo Escolar
  05_integrar_bases.py           Integra as bases e cria as variáveis
  06_analise_exploratoria.py     Gera gráficos e correlações
  07_regressao_linear.py         Regressão linear (OLS)
  08_random_forest.py            Random Forest e importância das variáveis
```

## Artigo

O artigo completo, com a metodologia, as figuras e as tabelas, está em `ARTIGO.pdf`.
