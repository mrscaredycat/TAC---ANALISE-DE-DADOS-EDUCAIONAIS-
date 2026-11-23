
import time
import subprocess
import sys
from pathlib import Path

def verificar_zips():
    zips_candidatos = [
        "microdados_enem_2021.zip",
        "microdados_enem_2022.zip",
        "microdados_enem_2023.zip"
    ]
    for z in zips_candidatos:
        if Path(z).exists():
            return True
        for match in Path(".").glob(f"**/{z}"):
            if match.is_file():
                return True
    return False

def executar_tudo():
    print("=" * 75)
    print("PIPELINE CIENTÍFICO: ANÁLISE DE DADOS DO ENEM NO DF (UnB/CIC)")
    print("=" * 75)
    inicio_total = time.time()
    
    base_processada = Path("data/processed/base_final_modelagem.csv")
    tem_zips = verificar_zips()

    scripts_para_rodar = []

    if tem_zips and ("--full" in sys.argv or not base_processada.exists()):
        print("\n[MODO COMPLETO] Arquivos ZIP brutos detectados. Executando pipeline desde a extração bruta...")
        scripts_para_rodar = [
            ("src/03_filtrar_enem_df.py", "1/6. Filtrando microdados do ENEM para o DF (2021-2023)"),
            ("src/04_processar_censo_indicadores.py", "2/6. Processando Censo Escolar e Infraestrutura do DF"),
            ("src/05_integrar_bases.py", "3/6. Integrando bases e criando engenharia de atributos"),
            ("src/06_analise_exploratoria.py", "4/6. Gerando Heatmap e Gráficos Exploratórios"),
            ("src/07_regressao_linear.py", "5/6. Rodando Regressão Linear Múltipla (OLS)"),
            ("src/08_random_forest.py", "6/6. Rodando Random Forest e Feature Importance")
        ]
    elif base_processada.exists():
        print("\n[MODO RÁPIDO/REPRODUTÍVEL] Base final processada detectada em:")
        print(f" -> {base_processada.resolve()}")
        print("[INFO] Executando Análise Exploratória, Regressão OLS, Random Forest e Artigo em PDF...\n")
        scripts_para_rodar = [
            ("src/06_analise_exploratoria.py", "1/3. Gerando Heatmap e Gráficos Exploratórios (Figuras 1, 2 e 3)"),
            ("src/07_regressao_linear.py", "2/3. Ajustando Regressão Linear OLS (Tabela 1)"),
            ("src/08_random_forest.py", "3/3. Treinando Random Forest e Feature Importance (Figura 4 e Tabela 2)")
        ]
    else:
        print("\n[AVISO] Base processada e arquivos ZIP não encontrados!")
        print("Por favor, verifique se a pasta 'data/processed' contém 'base_final_modelagem.csv'.")
        return

    for script, descricao in scripts_para_rodar:
        print(f"\n>>> Executando: {descricao}...")
        inicio = time.time()
        res = subprocess.run([sys.executable, script])
        if res.returncode != 0:
            print(f"\n[ERRO] Falha na execução do script: {script}")
            return
        fim = time.time()
        print(f"    Concluído em: {fim - inicio:.1f} segundos.")
        
    print("\n" + "=" * 75)
    print(f"PIPELINE EXECUTADO COM SUCESSO! Tempo total: {time.time() - inicio_total:.1f}s")
    print("Arquivos gerados e atualizados:")
    print(" - Figuras prontas em:      resultados/figuras/")
    print(" - Tabelas estatísticas em: resultados/tabelas/")
    print("[INFO] O artigo final é compilado em LaTeX a partir de relatorio.tex -> ARTIGO.pdf")
    print("=" * 75)

if __name__ == "__main__":
    executar_tudo()
