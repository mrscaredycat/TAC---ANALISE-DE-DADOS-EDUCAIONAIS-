"""
================================================================================
Geração de Relatório Científico em PDF: Figuras, Algoritmos e Interpretações
Universidade de Brasília - UnB | Departamento de Ciência da Computação - CIC
================================================================================
"""

import sys
from pathlib import Path
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch

def gerar_pdf():
    caminho_saida = Path("resultados/Relatorio_Figuras_e_Algoritmos_ENEM_DF.pdf")
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    
    doc = SimpleDocTemplate(
        str(caminho_saida),
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm
    )

    styles = getSampleStyleSheet()
    
    # Estilos customizados
    titulo_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1a365d"),
        spaceAfter=6
    )
    
    subtitulo_style = ParagraphStyle(
        "DocSub",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2b6cb0"),
        spaceAfter=12
    )

    autores_style = ParagraphStyle(
        "Autores",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2d3748"),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        "SecaoH1",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#2c5282"),
        spaceBefore=10,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        "SecaoH2",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#2d3748"),
        spaceBefore=8,
        spaceAfter=4
    )

    texto_style = ParagraphStyle(
        "CorpoTexto",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1a202c"),
        spaceAfter=6
    )

    destaque_style = ParagraphStyle(
        "BoxDestaque",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1a365d"),
        backColor=colors.HexColor("#ebf8ff"),
        borderColor=colors.HexColor("#bee3f8"),
        borderWidth=1,
        borderPadding=8,
        spaceAfter=8,
        spaceBefore=4
    )

    tabela_cell_style = ParagraphStyle(
        "CellTexto",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#2d3748")
    )
    tabela_head_style = ParagraphStyle(
        "CellHead",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    elementos = []

    # -------------------------------------------------------------
    # Cabeçalho Oficial
    # -------------------------------------------------------------
    elementos.append(Paragraph("Universidade de Brasília – UnB", subtitulo_style))
    elementos.append(Paragraph("Departamento de Ciência da Computação – CIC", subtitulo_style))
    elementos.append(Paragraph("Guia Técnico: Figuras, Algoritmos e Resultados do Artigo Científico", titulo_style))
    elementos.append(Paragraph("<b>Tema:</b> Fatores Socioeconômicos, Escolares e o Desempenho em Matemática no ENEM (Distrito Federal: 2021–2023)", subtitulo_style))
    
    autores_texto = (
        "<b>Autores do Projeto:</b><br/>"
        "• Ana Caroline Freitas Brito — Matrícula: <b>242001526</b><br/>"
        "• Ana Sarah Nagata — Matrícula: <b>242023176</b><br/>"
        "• Kamily Silva Andrade Crispim — Matrícula: <b>242009945</b><br/>"
        "<b>Amostra Analisada:</b> 126.874 estudantes do Distrito Federal presentes na prova de Matemática."
    )
    elementos.append(Paragraph(autores_texto, autores_style))
    elementos.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2b6cb0"), spaceAfter=14))

    # -------------------------------------------------------------
    # Visão Geral: Onde a Nota de Matemática é Avaliada
    # -------------------------------------------------------------
    elementos.append(Paragraph("1. Onde e Como a Nota de Matemática Foi Avaliada?", h1_style))
    desc_mat = (
        "A <b>Nota de Matemática (NU_NOTA_MT)</b> é a <b>Variável Dependente (Y)</b> central de todo o estudo. "
        "Ela não é apenas uma coluna qualquer, mas o desfecho que todos os modelos tentam explicar e predizer:<br/>"
        "• <b>Na Filtragem:</b> Foram retidos exclusivamente participantes do DF com presença confirmada e nota válida em Matemática.<br/>"
        "• <b>Nas Barras Agrupadas:</b> A altura de cada barra representa a <b>mediana da nota de Matemática</b> de cada subgrupo.<br/>"
        "• <b>No Heatmap:</b> A primeira linha mede a correlação de Pearson de todos os fatores familiares e escolares com a nota de Matemática.<br/>"
        "• <b>Na Regressão Linear:</b> Os coeficientes medem quantos pontos a mais ou a menos em Matemática cada característica confere.<br/>"
        "• <b>No Random Forest:</b> O algoritmo de Machine Learning foi treinado para predizer a nota de Matemática de cada aluno."
    )
    elementos.append(Paragraph(desc_mat, destaque_style))
    elementos.append(Spacer(1, 10))

    # Função auxiliar para incluir imagem proporcional
    def adicionar_figura(nome_arquivo, max_largura=460, max_altura=260):
        caminho_img = Path("resultados/figuras") / nome_arquivo
        if caminho_img.exists():
            with PILImage.open(caminho_img) as img:
                w_orig, h_orig = img.size
                razao = min(max_largura / w_orig, max_altura / h_orig)
                w_final = w_orig * razao
                h_final = h_orig * razao
            return Image(str(caminho_img), width=w_final, height=h_final)
        return Paragraph(f"<i>[Imagem {nome_arquivo} não encontrada]</i>", texto_style)

    # -------------------------------------------------------------
    # Figura 1: Heatmap
    # -------------------------------------------------------------
    elementos.append(PageBreak())
    elementos.append(Paragraph("2. Figura 1: Mapa de Calor de Correlações (Heatmap)", h1_style))
    elementos.append(Paragraph("<b>Arquivo:</b> <code>heatmap_correlacoes.png</code> | <b>Seção do Artigo:</b> Seção 4.1 (Análise Exploratória)", h2_style))
    
    img_heatmap = adicionar_figura("heatmap_correlacoes.png", max_largura=460, max_altura=250)
    elementos.append(img_heatmap)
    elementos.append(Spacer(1, 8))

    texto_f1 = (
        "<b>• Algoritmo / Método Utilizado:</b> Coeficiente de Correlação Linear de Pearson (<i>r</i>), "
        "cruzando variáveis contínuas e ordinais padronizadas.<br/>"
        "<b>• O que a figura está fazendo:</b> Cruza as variáveis do <b>Inep</b> (Nota de Matemática, Escolaridade do Pai e da Mãe, "
        "Renda, Computador, Internet, Infraestrutura da Escola) com o <b>PIB per capita do DF do IBGE</b> (R$ 92,7 mil a R$ 129,7 mil).<br/>"
        "<b>• Interpretação dos Resultados:</b> A nota de Matemática apresenta fortes correlações positivas com a <b>Renda Familiar (r = 0,47)</b>, "
        "a <b>Escolaridade do Pai (r = 0,38)</b>, a <b>Escolaridade da Mãe (r = 0,36)</b> e a posse de <b>Computador (r = 0,33)</b>. "
        "Isso confirma empiricamente a teoria de Bourdieu sobre o peso do capital cultural e econômico familiar."
    )
    elementos.append(Paragraph(texto_f1, texto_style))

    # -------------------------------------------------------------
    # Figura 2: Barras Agrupadas - Rede Pública vs Privada
    # -------------------------------------------------------------
    elementos.append(PageBreak())
    elementos.append(Paragraph("3. Figura 2: Mediana da Nota de Matemática por Estudo dos Pais e Rede", h1_style))
    elementos.append(Paragraph("<b>Arquivo:</b> <code>barras_mediana_escolaridade_rede.png</code> | <b>Seção do Artigo:</b> Seção 4.1", h2_style))
    
    img_rede = adicionar_figura("barras_mediana_escolaridade_rede.png", max_largura=460, max_altura=240)
    elementos.append(img_rede)
    elementos.append(Spacer(1, 8))

    texto_f2 = (
        "<b>• Algoritmo / Método Utilizado:</b> Agregação Estatística Descritiva Condicional focada na <b>MEDIANA</b> (robusta a outliers).<br/>"
        "<b>• O que a figura está fazendo:</b> Compara a nota mediana de Matemática entre estudantes de <b>Escolas Públicas</b> (azul) "
        "e <b>Escolas Privadas</b> (vermelho) dentro de cada nível de escolaridade dos pais (de 'Sem estudo' até 'Pós-graduação').<br/>"
        "<b>• Interpretação dos Resultados:</b> Revela duas desigualdades simultâneas: "
        "(1) O efeito do capital cultural familiar: mesmo dentro da escola pública, a nota mediana sobe de 435,5 (pais sem estudo) "
        "para mais de 550 pontos (pais com ensino superior); "
        "(2) O abismo estrutural: em qualquer nível de escolaridade dos pais, os alunos de escolas privadas obtêm desempenho expressivamente superior."
    )
    elementos.append(Paragraph(texto_f2, texto_style))

    # -------------------------------------------------------------
    # Figura 3: Barras Agrupadas - Posse de Computador / Recursos Digitais
    # -------------------------------------------------------------
    elementos.append(PageBreak())
    elementos.append(Paragraph("4. Figura 3: Mediana da Nota por Estudo dos Pais e Posse de Computador", h1_style))
    elementos.append(Paragraph("<b>Arquivo:</b> <code>barras_mediana_escolaridade_computador.png</code> | <b>Seção do Artigo:</b> Seção 4.1", h2_style))
    
    img_pc = adicionar_figura("barras_mediana_escolaridade_computador.png", max_largura=460, max_altura=240)
    elementos.append(img_pc)
    elementos.append(Spacer(1, 8))

    texto_f3 = (
        "<b>• Algoritmo / Método Utilizado:</b> Agregação Estatística Condicional pela <b>Mediana</b> com estratificação por tecnologia doméstica.<br/>"
        "<b>• O que a figura está fazendo:</b> Isola o efeito da posse de computador em casa (item Q024 do ENEM) dentro de cada faixa de instrução dos pais.<br/>"
        "<b>• Interpretação dos Resultados:</b> Estudantes que possuem computador em casa alcançam mediana de Matemática de <b>575,5 pontos</b>, "
        "contra apenas <b>474,3 pontos</b> daqueles que não possuem (diferença direta de 101,2 pontos na mediana). "
        "Isso demonstra que o acesso digital funciona como catalisador do aprendizado autônomo e preparo para o exame."
    )
    elementos.append(Paragraph(texto_f3, texto_style))

    # -------------------------------------------------------------
    # Figura 4: Ranking do Random Forest
    # -------------------------------------------------------------
    elementos.append(PageBreak())
    elementos.append(Paragraph("5. Figura 4: Ranking de Importância Relativa (Random Forest)", h1_style))
    elementos.append(Paragraph("<b>Arquivo:</b> <code>ranking_importancia_variaveis.png</code> | <b>Seção do Artigo:</b> Seção 4.3 (Machine Learning)", h2_style))
    
    img_rf = adicionar_figura("ranking_importancia_variaveis.png", max_largura=460, max_altura=240)
    elementos.append(img_rf)
    elementos.append(Spacer(1, 8))

    texto_f4 = (
        "<b>• Algoritmo / Método Utilizado:</b> <b>Random Forest Regressor</b> (ensemble supervisionado com 100 árvores de decisão) "
        "utilizando o critério de redução de variância <b>MDI (Mean Decrease in Impurity)</b>.<br/>"
        "<b>• O que a figura está fazendo:</b> Ranqueia matematicamente qual fator tem o maior poder preditivo sobre a nota de Matemática "
        "após treinar com 70% dos dados (88.811 alunos) e testar com 30% (38.063 alunos).<br/>"
        "<b>• Interpretação dos Resultados:</b><br/>"
        "  1º <b>Renda Familiar Mensal: 64,05%</b> da importância preditiva do modelo.<br/>"
        "  2º <b>Escolaridade do Pai: 8,22%</b>.<br/>"
        "  3º <b>Escolaridade da Mãe: 7,79%</b> (Escolaridade dos pais combinada soma <b>16,01%</b>).<br/>"
        "  4º <b>Ano do Exame: 4,87%</b> | 5º <b>Computador em Casa: 3,28%</b> | 6º <b>Sexo Feminino: 3,17%</b>.<br/>"
        "  7º <b>Cor/Raça PPI: 2,56%</b> | 8º <b>Escola Urbana: 2,42%</b> | 9º <b>Rede Privada: 1,83%</b>.<br/>"
        "<b>Métricas no Conjunto de Teste:</b> R² = 0,2896 | RMSE = 108,61 pontos | MAE = 85,60 pontos."
    )
    elementos.append(Paragraph(texto_f4, texto_style))

    # -------------------------------------------------------------
    # Tabela 1: Médias e Medianas por Subcategoria
    # -------------------------------------------------------------
    elementos.append(PageBreak())
    elementos.append(Paragraph("6. Tabela Oficial: Médias e Medianas por Subcategoria", h1_style))
    elementos.append(Paragraph("<b>Arquivo:</b> <code>medias_notas_por_subcategoria.csv</code> | <b>Exigência expressa do TAC/UnB</b>", h2_style))
    
    dados_tabela = [
        [
            Paragraph("<b>Dimensão</b>", tabela_head_style),
            Paragraph("<b>Subcategoria</b>", tabela_head_style),
            Paragraph("<b>Total Alunos (N)</b>", tabela_head_style),
            Paragraph("<b>Nota Média</b>", tabela_head_style),
            Paragraph("<b>Nota Mediana</b>", tabela_head_style),
            Paragraph("<b>Desvio Padrão</b>", tabela_head_style)
        ],
        [Paragraph("Rede de Ensino", tabela_cell_style), Paragraph("Privada", tabela_cell_style), Paragraph("18.377", tabela_cell_style), Paragraph("621,11", tabela_cell_style), Paragraph("629,90", tabela_cell_style), Paragraph("119,88", tabela_cell_style)],
        [Paragraph("Rede de Ensino", tabela_cell_style), Paragraph("Federal (IFB)", tabela_cell_style), Paragraph("2.207", tabela_cell_style), Paragraph("600,99", tabela_cell_style), Paragraph("600,50", tabela_cell_style), Paragraph("127,23", tabela_cell_style)],
        [Paragraph("Rede de Ensino", tabela_cell_style), Paragraph("Pública Distrital", tabela_cell_style), Paragraph("26.063", tabela_cell_style), Paragraph("511,63", tabela_cell_style), Paragraph("501,30", tabela_cell_style), Paragraph("101,13", tabela_cell_style)],
        [Paragraph("Escolaridade Pais", tabela_cell_style), Paragraph("Pós-graduação", tabela_cell_style), Paragraph("39.018", tabela_cell_style), Paragraph("623,73", tabela_cell_style), Paragraph("633,90", tabela_cell_style), Paragraph("129,88", tabela_cell_style)],
        [Paragraph("Escolaridade Pais", tabela_cell_style), Paragraph("Ensino Superior", tabela_cell_style), Paragraph("27.731", tabela_cell_style), Paragraph("586,20", tabela_cell_style), Paragraph("588,10", tabela_cell_style), Paragraph("126,30", tabela_cell_style)],
        [Paragraph("Escolaridade Pais", tabela_cell_style), Paragraph("Ensino Médio", tabela_cell_style), Paragraph("42.617", tabela_cell_style), Paragraph("521,14", tabela_cell_style), Paragraph("509,50", tabela_cell_style), Paragraph("109,27", tabela_cell_style)],
        [Paragraph("Escolaridade Pais", tabela_cell_style), Paragraph("Fundamental II", tabela_cell_style), Paragraph("8.610", tabela_cell_style), Paragraph("490,27", tabela_cell_style), Paragraph("475,80", tabela_cell_style), Paragraph("99,33", tabela_cell_style)],
        [Paragraph("Escolaridade Pais", tabela_cell_style), Paragraph("Fundamental I", tabela_cell_style), Paragraph("8.271", tabela_cell_style), Paragraph("475,64", tabela_cell_style), Paragraph("460,40", tabela_cell_style), Paragraph("94,68", tabela_cell_style)],
        [Paragraph("Escolaridade Pais", tabela_cell_style), Paragraph("Sem estudo", tabela_cell_style), Paragraph("1.574", tabela_cell_style), Paragraph("448,79", tabela_cell_style), Paragraph("435,55", tabela_cell_style), Paragraph("83,26", tabela_cell_style)],
        [Paragraph("Recursos Digitais", tabela_cell_style), Paragraph("Possui Computador", tabela_cell_style), Paragraph("105.100", tabela_cell_style), Paragraph("577,98", tabela_cell_style), Paragraph("575,50", tabela_cell_style), Paragraph("129,04", tabela_cell_style)],
        [Paragraph("Recursos Digitais", tabela_cell_style), Paragraph("Não Possui", tabela_cell_style), Paragraph("35.349", tabela_cell_style), Paragraph("487,51", tabela_cell_style), Paragraph("474,30", tabela_cell_style), Paragraph("99,45", tabela_cell_style)],
        [Paragraph("Localização", tabela_cell_style), Paragraph("Escola Urbana", tabela_cell_style), Paragraph("45.748", tabela_cell_style), Paragraph("559,98", tabela_cell_style), Paragraph("552,50", tabela_cell_style), Paragraph("122,75", tabela_cell_style)],
        [Paragraph("Localização", tabela_cell_style), Paragraph("Escola Rural", tabela_cell_style), Paragraph("902", tabela_cell_style), Paragraph("508,52", tabela_cell_style), Paragraph("503,40", tabela_cell_style), Paragraph("94,37", tabela_cell_style)],
        [Paragraph("Cor / Raça", tabela_cell_style), Paragraph("Brancos/Amarelos", tabela_cell_style), Paragraph("65.539", tabela_cell_style), Paragraph("587,69", tabela_cell_style), Paragraph("587,90", tabela_cell_style), Paragraph("132,28", tabela_cell_style)],
        [Paragraph("Cor / Raça", tabela_cell_style), Paragraph("Pretos/Pardos/Indígenas (PPI)", tabela_cell_style), Paragraph("74.910", tabela_cell_style), Paragraph("526,79", tabela_cell_style), Paragraph("511,20", tabela_cell_style), Paragraph("117,81", tabela_cell_style)],
    ]

    tabela_subcat = Table(dados_tabela, colWidths=[90, 115, 65, 60, 60, 60])
    tabela_subcat.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5282")),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elementos.append(tabela_subcat)
    elementos.append(Spacer(1, 14))

    # -------------------------------------------------------------
    # Tabela 2: Regressão Linear Múltipla (OLS)
    # -------------------------------------------------------------
    elementos.append(Paragraph("7. Tabela Oficial: Coeficientes da Regressão Linear Múltipla (OLS)", h1_style))
    elementos.append(Paragraph("<b>Arquivo:</b> <code>regressao_linear_coeficientes.csv</code> | <b>Seção do Artigo:</b> Seção 4.2", h2_style))
    
    dados_regressao = [
        [
            Paragraph("<b>Fator Socioeconômico / Escolar</b>", tabela_head_style),
            Paragraph("<b>Coeficiente (β)</b>", tabela_head_style),
            Paragraph("<b>Erro Padrão</b>", tabela_head_style),
            Paragraph("<b>Estatística t</b>", tabela_head_style),
            Paragraph("<b>p-valor</b>", tabela_head_style),
            Paragraph("<b>IC 95%</b>", tabela_head_style)
        ],
        [Paragraph("Intercepto (Constante β0)", tabela_cell_style), Paragraph("373,13", tabela_cell_style), Paragraph("2,17", tabela_cell_style), Paragraph("171,58", tabela_cell_style), Paragraph("&lt; 0,001", tabela_cell_style), Paragraph("[368,86; 377,39]", tabela_cell_style)],
        [Paragraph("Escolaridade Pai (anos de estudo)", tabela_cell_style), Paragraph("+4,08", tabela_cell_style), Paragraph("0,09", tabela_cell_style), Paragraph("46,21", tabela_cell_style), Paragraph("&lt; 0,001", tabela_cell_style), Paragraph("[3,91; 4,26]", tabela_cell_style)],
        [Paragraph("Escolaridade Mãe (anos de estudo)", tabela_cell_style), Paragraph("+3,65", tabela_cell_style), Paragraph("0,09", tabela_cell_style), Paragraph("38,91", tabela_cell_style), Paragraph("&lt; 0,001", tabela_cell_style), Paragraph("[3,47; 3,84]", tabela_cell_style)],
        [Paragraph("Renda Familiar Mensal (Log)", tabela_cell_style), Paragraph("+13,51", tabela_cell_style), Paragraph("0,22", tabela_cell_style), Paragraph("61,67", tabela_cell_style), Paragraph("&lt; 0,001", tabela_cell_style), Paragraph("[13,08; 13,94]", tabela_cell_style)],
        [Paragraph("Possui Computador em Casa", tabela_cell_style), Paragraph("+27,46", tabela_cell_style), Paragraph("0,84", tabela_cell_style), Paragraph("32,70", tabela_cell_style), Paragraph("&lt; 0,001", tabela_cell_style), Paragraph("[25,82; 29,11]", tabela_cell_style)],
        [Paragraph("Rede Privada (vs Pública)", tabela_cell_style), Paragraph("+44,20", tabela_cell_style), Paragraph("1,15", tabela_cell_style), Paragraph("38,31", tabela_cell_style), Paragraph("&lt; 0,001", tabela_cell_style), Paragraph("[41,94; 46,46]", tabela_cell_style)],
        [Paragraph("Rede Federal IFB (vs Pública)", tabela_cell_style), Paragraph("+45,39", tabela_cell_style), Paragraph("2,53", tabela_cell_style), Paragraph("17,93", tabela_cell_style), Paragraph("&lt; 0,001", tabela_cell_style), Paragraph("[40,43; 50,35]", tabela_cell_style)],
        [Paragraph("Cor/Raça PPI (Pretos/Pardos/Ind.)", tabela_cell_style), Paragraph("-24,19", tabela_cell_style), Paragraph("0,65", tabela_cell_style), Paragraph("-37,11", tabela_cell_style), Paragraph("&lt; 0,001", tabela_cell_style), Paragraph("[-25,47; -22,91]", tabela_cell_style)],
        [Paragraph("Sexo Feminino (vs Masculino)", tabela_cell_style), Paragraph("-32,85", tabela_cell_style), Paragraph("0,64", tabela_cell_style), Paragraph("-51,51", tabela_cell_style), Paragraph("&lt; 0,001", tabela_cell_style), Paragraph("[-34,10; -31,60]", tabela_cell_style)],
    ]

    tabela_reg = Table(dados_regressao, colWidths=[150, 60, 50, 50, 50, 90])
    tabela_reg.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5282")),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elementos.append(tabela_reg)
    elementos.append(Spacer(1, 8))
    elementos.append(Paragraph("<b>Métricas Globais da Regressão:</b> R² = 0,2784 | R² Ajustado = 0,2783 | F = 4.079 (p &lt; 0,001) | N = 126.874 estudantes.", destaque_style))

    doc.build(elementos)
    print(f"\n[SUCESSO] Relatório PDF gerado em: {caminho_saida}")
    return caminho_saida

if __name__ == "__main__":
    gerar_pdf()
