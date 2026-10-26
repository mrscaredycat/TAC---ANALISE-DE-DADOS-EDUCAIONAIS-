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
    print("2. VERIFICANDO ARQUIVOS DE DADOS (ZIPS E PLANILHAS):")
    print("=" * 70)
    pastas_para_olhar = [Path("."), Path("data/raw"), Path("2021-2023")]
    zips_encontrados = {}
    
    for pasta in pastas_para_olhar:
        if pasta.exists():
            for arq in pasta.glob("*.zip"):
                if arq.name not in zips_encontrados:
                    zips_encontrados[arq.name] = arq
                    
    if not zips_encontrados:
        print("Nenhum arquivo .zip encontrado na raiz ou em data/raw/.")
    else:
        for nome, caminho in sorted(zips_encontrados.items()):
            tamanho_mb = caminho.stat().st_size / (1024 * 1024)
            print(f" [ENCONTRADO] {nome.ljust(35)} ({tamanho_mb:6.1f} MB) em {caminho.parent}")
    print("=" * 70)

if __name__ == "__main__":
    verificar_ambiente()
    verificar_arquivos_dados()
