"""
================================================================================
Pipeline Completo: Artigo ENEM (2021 a 2023) - Distrito Federal
================================================================================

Este script executa todas as etapas em sequência:
1. `03_filtrar_enem_df.py`           -> Filtra dados do DF direto dos zips
2. `04_processar_censo_indicadores.py` -> Extrai indicadores escolares do DF
3. `05_integrar_bases.py`            -> Faz a engenharia de atributos e merge
4. `06_analise_exploratoria.py`      -> Cria os gráficos para a Seção 4.1
5. `07_regressao_linear.py`          -> Gera os coeficientes para a Seção 4.2
6. `08_random_forest.py`             -> Gera o ranking para a Seção 4.3
"""

import time
import subprocess
import sys

SCRIPTS = [
    ("src/03_filtrar_enem_df.py", "1/6. Filtrando microdados do ENEM para o DF (2021-2023)"),
    ("src/04_processar_censo_indicadores.py", "2/6. Processando Censo Escolar e Infraestrutura do DF"),
    ("src/05_integrar_bases.py", "3/6. Integrando bases e criando engenharia de atributos"),
    ("src/06_analise_exploratoria.py", "4/6. Gerando Heatmap e Gráficos Exploratórios"),
    ("src/07_regressao_linear.py", "5/6. Rodando Regressão Linear Múltipla (OLS)"),
    ("src/08_random_forest.py", "6/6. Rodando Random Forest e Feature Importance")
]

def executar_tudo():
    print("=" * 70)
    print("INICIANDO EXECUÇÃO COMPLETA DO PIPELINE CIENTÍFICO")
    print("=" * 70)
    inicio_total = time.time()
    
    for script, descricao in SCRIPTS:
        print(f"\n>>> Executando: {descricao}...")
        inicio = time.time()
        res = subprocess.run([sys.executable, script])
        if res.returncode != 0:
            print(f"\n[ERRO] Falha na execução do script: {script}")
            return
        fim = time.time()
        print(f"Tempo decorrido: {fim - inicio:.1f} segundos.")
        
    print("\n" + "=" * 70)
    print(f"PIPELINE CONCLUÍDO COM SUCESSO! Tempo total: {time.time() - inicio_total:.1f}s")
    print("Verifique os resultados gerados:")
    print(" - Figuras do artigo em: resultados/figuras/")
    print(" - Tabelas estatísticas em: resultados/tabelas/")
    print("=" * 70)

if __name__ == "__main__":
    executar_tudo()
