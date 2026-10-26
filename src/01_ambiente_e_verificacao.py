"""
================================================================================
Etapa 01: Verificação de Ambiente e de Arquivos Brutos
Artigo: Fatores Socioeconômicos e Educacionais e o Desempenho no ENEM (DF)
================================================================================

Este script tem como objetivos:
1. Testar se as bibliotecas essenciais para análise de dados e machine learning estão instaladas.
2. Mapear os arquivos presentes na pasta `data/raw/` (microdados do ENEM, Censo Escolar, INSE, PIB, etc.).
3. Informar o status de prontidão para iniciarmos o processamento.
"""

import sys
import os
from pathlib import Path

# Lista de pacotes necessários para o projeto
PACOTES_REQUERIDOS = [
    ("pandas", "Manipulação de dados em tabelas"),
    ("numpy", "Operações numéricas matriciais"),
    ("matplotlib", "Geração de gráficos estáticos"),
    ("seaborn", "Gráficos estatísticos e heatmaps"),
    ("sklearn", "Scikit-Learn: Regressão linear e Random Forest"),
    ("statsmodels", "Estatísticas detalhadas de regressão (valores-p, R2 ajustado)"),
    ("openpyxl", "Leitura de planilhas Excel (.xlsx) caso aplicável")
]

def verificar_ambiente():
    print("=" * 70)
    print("1. VERIFICANDO BIBLIOTECAS PYTHON INSTALADAS:")
    print("=" * 70)
    faltantes = []
    for modulo, descricao in PACOTES_REQUERIDOS:
        try:
            __import__(modulo)
            print(f" [OK] {modulo.ljust(15)} - {descricao}")
        except ImportError:
            print(f" [FALTANDO] {modulo.ljust(15)} - {descricao}")
            faltantes.append(modulo)
    
    if faltantes:
        print("\nPara instalar os pacotes faltantes, execute no terminal:")
        pacotes_pip = [p if p != "sklearn" else "scikit-learn" for p in faltantes]
        print(f"pip install {' '.join(pacotes_pip)}\n")
    else:
        print("\nTodas as bibliotecas estão disponíveis!\n")

def verificar_arquivos_dados():
    print("=" * 70)
    print("2. VERIFICANDO ARQUIVOS EM data/raw/ :")
    print("=" * 70)
    pasta_raw = Path("data/raw")
    if not pasta_raw.exists():
        print("Pasta data/raw ainda não foi criada.")
        return

    arquivos = list(pasta_raw.glob("*"))
    if not arquivos:
        print("A pasta 'data/raw' está vazia.")
        print("Aqui colocaremos os arquivos baixados do Inep (ENEM, Censo, INSE) e do IBGE.")
    else:
        for arq in arquivos:
            tamanho_mb = arq.stat().st_size / (1024 * 1024)
            print(f" - {arq.name} ({tamanho_mb:.2f} MB)")
    print("=" * 70)

if __name__ == "__main__":
    verificar_ambiente()
    verificar_arquivos_dados()
