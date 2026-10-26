"""
================================================================================
Compilador do Artigo Científico Completo em PDF (Duas Colunas / Padrão SBC/IEEE)
Universidade de Brasília - UnB | Departamento de Ciência da Computação - CIC
Autores: Ana Caroline Freitas Brito, Ana Sarah Nagata, Kamily Silva Andrade Crispim
================================================================================
"""

import sys
from pathlib import Path
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, Table, TableStyle, FrameBreak, PageBreak, HRFlowable, NextPageTemplate
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT

def gerar_artigo():
    caminho_pdf = Path("Artigo_Completo_ENEM_DF_UnB.pdf")
    
    # Dimensões da página A4
    page_w, page_h = A4 # 595.27 x 841.89
    margin_x = 42 # ~ 1.5 cm
    margin_y = 42 # ~ 1.5 cm
    col_gap = 16
    avail_w = page_w - (2 * margin_x) # 511.27
    col_w = (avail_w - col_gap) / 2 # 247.63
    avail_h = page_h - (2 * margin_y) # 757.89

    # Configuração dos Frames (Page 1 vs Pages Seguintes)
    # Página 1: Top frame para Título e Autores (altura 125 pt) + duas colunas embaixo
    h_top = 120
    gap_top = 10
    h_b1 = avail_h - h_top - gap_top

    f_top = Frame(margin_x, page_h - margin_y - h_top, avail_w, h_top, id='f_top',
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    f_b1 = Frame(margin_x, margin_y, col_w, h_b1, id='f_b1',
                 leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    f_b2 = Frame(margin_x + col_w + col_gap, margin_y, col_w, h_b1, id='f_b2',
                 leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    # Páginas Seguintes: Duas colunas ocupando a altura total
    f_lat1 = Frame(margin_x, margin_y, col_w, avail_h, id='f_lat1',
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    f_lat2 = Frame(margin_x + col_w + col_gap, margin_y, col_w, avail_h, id='f_lat2',
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    doc = BaseDocTemplate(str(caminho_pdf), pagesize=A4, leftMargin=margin_x, rightMargin=margin_x, topMargin=margin_y, bottomMargin=margin_y)
    
    template_first = PageTemplate(id='FirstPage', frames=[f_top, f_b1, f_b2])
    template_later = PageTemplate(id='LaterPages', frames=[f_lat1, f_lat2])
    doc.addPageTemplates([template_first, template_later])

    # Estilos Tipográficos Padrão Artigo Científico (SBC / IEEE)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ArtTitle",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=6
    )

    authors_style = ParagraphStyle(
        "ArtAuthors",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11.5,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=2
    )

    affil_style = ParagraphStyle(
        "ArtAffil",
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#475569"),
        spaceAfter=6
    )

    resumo_title_style = ParagraphStyle(
        "ResumoTitle",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=2,
        spaceAfter=2
    )

    resumo_body_style = ParagraphStyle(
        "ResumoBody",
        fontName="Helvetica",
        fontSize=7.8,
        leading=10.5,
        alignment=TA_JUSTIFY,
        firstLineIndent=10,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=4
    )

    h1_style = ParagraphStyle(
        "Heading1_Artigo",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12.5,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Heading2_Artigo",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11.5,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body_Artigo",
        fontName="Times-Roman",
        fontSize=8.5,
        leading=11.5,
        alignment=TA_JUSTIFY,
        firstLineIndent=12,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=3
    )

    caption_style = ParagraphStyle(
        "Caption_Artigo",
        fontName="Helvetica-Bold",
        fontSize=7.2,
        leading=9.2,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#334155"),
        spaceBefore=2,
        spaceAfter=5
    )

    tbl_head = ParagraphStyle("TH", fontName="Helvetica-Bold", fontSize=6.5, leading=8, alignment=TA_CENTER, textColor=colors.HexColor("#0f172a"))
    tbl_cell = ParagraphStyle("TD", fontName="Times-Roman", fontSize=6.5, leading=8, alignment=TA_LEFT, textColor=colors.HexColor("#0f172a"))
    tbl_num = ParagraphStyle("TDN", fontName="Times-Roman", fontSize=6.5, leading=8, alignment=TA_RIGHT, textColor=colors.HexColor("#0f172a"))

    story = []

    # -------------------------------------------------------------
    # TOPO DA PÁGINA 1: Título, Autores e Afiliação
    # -------------------------------------------------------------
    titulo_texto = "Fatores Socioeconômicos, Escolares e o Desempenho em Matemática no ENEM: Uma Análise Empírica e Preditiva no Distrito Federal (2021–2023)"
    story.append(Paragraph(titulo_texto, title_style))
    
    autores_texto = "Ana Caroline Freitas Brito (242001526), Ana Sarah Nagata (242023176), Kamily Silva Andrade Crispim (242009945)"
    story.append(Paragraph(autores_texto, authors_style))

    inst_texto = "Departamento de Ciência da Computação (CIC) – Universidade de Brasília (UnB)<br/>Brasília – DF – Brasil"
    story.append(Paragraph(inst_texto, affil_style))
    story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#94a3b8"), spaceAfter=4))
    
    # Comuta para as colunas seguintes nas próximas páginas
    story.append(NextPageTemplate('LaterPages'))
    # Salta do frame de topo para a Coluna 1 da Página 1
    story.append(FrameBreak())

    # -------------------------------------------------------------
    # COLUNA 1: Resumo e Palavras-chave
    # -------------------------------------------------------------
    story.append(Paragraph("Resumo", resumo_title_style))
    resumo_texto = (
        "O Exame Nacional do Ensino Médio (ENEM) é o principal mecanismo de acesso ao ensino superior no Brasil, "
        "e seus resultados frequentemente refletem disparidades socioeconômicas e educacionais. Este trabalho investiga "
        "como fatores familiares (escolaridade dos pais e renda) e escolares (rede de ensino, localização e infraestrutura), "
        "em conjunto com o contexto macroeconômico do DF (PIB per capita do IBGE), associam-se ao desempenho em Matemática "
        "dos estudantes do Distrito Federal no ENEM entre 2021 e 2023, avaliando em que medida essas relações variam entre grupos. "
        "Utilizam-se os microdados do ENEM, o Censo Escolar da Educação Básica e indicadores econômicos oficiais. A metodologia "
        "combina exploração visual (matriz de correlação de Pearson e gráficos de barras com mediana), regressão linear múltipla (OLS) "
        "e aprendizado de máquina supervisionado com Random Forest Regressor, tendo a nota de Matemática como variável dependente. "
        "A amostra reúne 126.874 estudantes assíduos. Os resultados evidenciam que a renda familiar e o capital cultural dos pais "
        "explicam mais de 80% da importância preditiva do desempenho, e que a rede privada e a posse de computador conferem vantagens "
        "líquidas substantivas mesmo após controle multivariado, oferecendo subsídios para políticas de equidade educacional."
    )
    story.append(Paragraph(resumo_texto, resumo_body_style))

    kw_texto = "<b>Palavras-chave:</b> ENEM; Matemática; desigualdade educacional; nível socioeconômico; mineração de dados educacionais; Random Forest."
    story.append(Paragraph(kw_texto, resumo_body_style))
    story.append(Spacer(1, 4))

    # -------------------------------------------------------------
    # 1. Introdução (Texto Original do Aluno)
    # -------------------------------------------------------------
    story.append(Paragraph("1. Introdução", h1_style))
    p1 = (
        "O ENEM, criado em 1998, tornou-se o principal mecanismo de acesso ao ensino superior brasileiro, sendo usado por "
        "universidades públicas via SISU e por programas governamentais como o ProUni e o Fies. Por reunir milhões de participantes "
        "todos os anos, constitui uma das fontes mais ricas para investigar o desempenho de concluintes da educação básica e "
        "as desigualdades estruturais que os cercam."
    )
    story.append(Paragraph(p1, body_style))

    p2 = (
        "A literatura demonstra que o rendimento acadêmico no exame não decorre unicamente do esforço individual. Estudos com "
        "microdados do Inep apontam que o desempenho dos candidatos correlaciona-se estreitamente com a origem familiar, a tipologia "
        "da escola frequentada e a disponibilidade de recursos pedagógicos e tecnológicos no domicílio. Nesse debate sociológico e "
        "educacional, a escolaridade dos pais é recorrentemente identificada como um dos mais potentes preditores do sucesso acadêmico."
    )
    story.append(Paragraph(p2, body_style))

    p3 = (
        "No contexto brasileiro, a clivagem entre redes pública e privada configura um dos eixos mais críticos de disparidade. Na "
        "avaliação internacional PISA 2018, escolas privadas registraram resultados amplamente superiores aos da rede pública em "
        "Matemática, Ciências e Leitura (OECD, 2018), padrão igualmente documentado por Moraes e Belluzzo (2014). Esse diagnóstico "
        "fundamentou ações afirmativas indispensáveis, como a Lei de Cotas (Lei nº 12.711/2012), que democratizou o ingresso de egressos "
        "da escola pública nas universidades federais. Contudo, pesquisas sobre trajetórias universitárias indicam que déficits de "
        "preparo formativo prévio continuam a condicionar o rendimento dos estudantes após o ingresso, reforçando a urgência de diagnosticar "
        "essas assimetrias ainda na educação básica."
    )
    story.append(Paragraph(p3, body_style))

    p4 = (
        "O Distrito Federal configura um laboratório socioespacial de especial relevância. Reúne um dos maiores PIBs per capita do "
        "país e, simultaneamente, aguda segregação socioeconômica entre suas regiões administrativas, com redes pública e privada coabitando "
        "o mesmo território federativo. Essa configuração viabiliza examinar desigualdades educacionais em um contexto territorial concentrado, "
        "imune à heterogeneidade macrorregional observada em amostras de abrangência nacional."
    )
    story.append(Paragraph(p4, body_style))

    p5 = (
        "Optou-se por analisar exclusivamente o desempenho em Matemática em virtude de sua estreita vinculação formativa com as áreas "
        "STEM e com a educação em computação. Sendo o ENEM a porta mestra para graduações tecnológicas, quantificar os fatores associados "
        "à nota de Matemática permite mapear os gargalos prévios que chegam ao ensino superior. Ademais, concentrar a análise em uma única "
        "área de conhecimento evita confundimentos entre domínios distintos e confere precisão às comparações intergrupais."
    )
    story.append(Paragraph(p5, body_style))

    p6 = (
        "Assim, a questão norteadora desta pesquisa é: <i>Como fatores socioeconômicos e educacionais, incluindo a escolaridade dos pais "
        "e as características da escola (rede, localização e infraestrutura), se associam ao desempenho em Matemática dos estudantes do "
        "Distrito Federal no ENEM, e em que medida essas relações variam entre diferentes grupos e contextos no triênio 2021–2023?</i> "
        "Para respondê-la, articula-se uma abordagem em três frentes: exploração visual descritiva por medianas, regressão linear "
        "múltipla e Random Forest Regressor."
    )
    story.append(Paragraph(p6, body_style))

    # -------------------------------------------------------------
    # 2. Background
    # -------------------------------------------------------------
    story.append(Paragraph("2. Background", h1_style))
    story.append(Paragraph("2.1 Origem social, escola e desigualdade de desempenho", h2_style))
    p_bg1 = (
        "A concepção de que o rendimento escolar traduz a origem social possui sólida tradição na sociologia da educação. Bourdieu e "
        "Passeron (1970) conceituam a escola como instituição reprodutora de desigualdades, na medida em que chancela o capital cultural "
        "transmitido pelo meio familiar. Nessa formulação, o nível instrucional dos pais opera como proxy do capital cultural incorporado "
        "e da ambiência pedagógica doméstica. Pesquisas empíricas com o ENEM no Ceará e no Nordeste confirmam que escolaridade dos genitores "
        "e renda domiciliar exercem impacto sistemático e positivo sobre as notas."
    )
    story.append(Paragraph(p_bg1, body_style))

    story.append(Paragraph("2.2 Rede, localização e infraestrutura escolar", h2_style))
    p_bg2 = (
        "Para além da família, o ambiente escolar modula as trajetórias formativas. A discrepância entre as redes pública e privada "
        "emerge reiteradamente em avaliações em larga escala, embora parte dessa distância resulte da seleção prévia de perfil socioeconômico "
        "atendido por cada subsistema. Torna-se imprescindível contrastar os indicadores de nível socioeconômico (INSE) com atributos "
        "estruturais concretos da escola, tais como localização (urbana ou rural), conectividade e laboratórios de informática e ciências."
    )
    story.append(Paragraph(p_bg2, body_style))

    story.append(Paragraph("2.3 Contexto territorial e econômico", h2_style))
    p_bg3 = (
        "O território escolar condiciona o leque de oportunidades: renda regional, acessibilidade a serviços públicos e conectividade variam "
        "de forma marcante no Distrito Federal. Estudos sobre o ENEM em outros recortes federativos comprovam clivagens espaciais notáveis. "
        "Incorporar a dimensão macroeconômica anual do DF viabiliza testar em que medida o contexto econômico se associa ao desempenho para "
        "além do perfil individual do candidato."
    )
    story.append(Paragraph(p_bg3, body_style))

    story.append(Paragraph("2.4 Mineração de dados educacionais e modelos preditivos", h2_style))
    p_bg4 = (
        "A Mineração de Dados Educacionais (EDM) mobiliza métodos computacionais e estatísticos sobre bases de larga escala para produzir "
        "conhecimento acionável a políticas públicas. Enquanto a regressão linear múltipla oferece alta interpretabilidade ao estimar "
        "coeficientes marginais constantes, algoritmos baseados em árvores como o Random Forest captam não linearidades e interações complexas, "
        "ranqueando a relevância relativa de cada atributo (feature importance). Neste estudo, ambas as técnicas se complementam."
    )
    story.append(Paragraph(p_bg4, body_style))

    # -------------------------------------------------------------
    # 2.5 Trabalhos Relacionados (NOVO! Integrando a Referência da UnB)
    # -------------------------------------------------------------
    story.append(Paragraph("2.5 Trabalhos Relacionados", h2_style))
    p_rel1 = (
        "No âmbito da educação em computação no Distrito Federal, destaca-se a pesquisa seminal de Silveira, Holanda e Ramos (2022), "
        "intitulada <i>'Analysis of Student Performance and Social-economic Data in Introductory Computer Science Courses at the University of Brasília'</i>, "
        "apresentada na IEEE Frontiers in Education Conference (FIE). Os autores aplicaram técnicas de Mineração de Dados Educacionais (EDM) "
        "e Modelos Lineares Generalizados (GLM) aos dados de calouros matriculados na disciplina de introdução à programação (CS1) nos quatro cursos "
        "do Departamento de Ciência da Computação da UnB (Ciência da Computação, Licenciatura em Computação, Engenharia de Computação e "
        "Engenharia Mecatrônica) entre 2012 e 2019."
    )
    story.append(Paragraph(p_rel1, body_style))

    p_rel2 = (
        "Aquele estudo revelou achados cruciais para o entendimento da evasão e da retenção acadêmica na UnB: o egresso de escola privada "
        "apresentou coeficiente positivo e significante no desempenho em programação (+0,796), ao passo que a vulnerabilidade socioeconômica "
        "(medida pela concessão de auxílio financeiro e alimentação subsidiada no campus) associou-se negativamente à taxa de aprovação (-0,768). "
        "Silveira et al. (2022) constataram ainda que, embora a Lei de Cotas tenha ampliado expressivamente a diversidade socioeconômica na universidade, "
        "os cotistas enfrentam maiores taxas de reprovação inicial nas matérias de exatas em decorrência de lacunas de preparo prévio acumuladas ao longo da educação básica."
    )
    story.append(Paragraph(p_rel2, body_style))

    p_rel3 = (
        "O presente trabalho dialoga diretamente com os achados de Silveira et al. (2022), porém recuando uma etapa estratégica na cadeia formativa: "
        "em vez de diagnosticar a retenção do estudante após seu ingresso na UnB, investigamos a **formação e os filtros na conclusão do ensino médio no próprio DF**. "
        "Ao decompor a nota de Matemática no ENEM por meio de regressão econométrica e aprendizado de máquina supervisionado, identificamos a magnitude exata "
        "com que o capital cultural familiar, o tipo de escola e a infraestrutura tecnológica doméstica estabelecem os diferenciais de proficiência que, "
        "posteriormente, chegam às salas de aula do ensino superior em computação da capital federal."
    )
    story.append(Paragraph(p_rel3, body_style))

    # -------------------------------------------------------------
    # 3.0 Metodologia
    # -------------------------------------------------------------
    story.append(Paragraph("3.0 Metodologia", h1_style))
    story.append(Paragraph("3.1 Amostra e Coleta em Streaming", h2_style))
    p_met1 = (
        "A base de dados integra três fontes abertas oficiais referentes ao triênio 2021–2023: os microdados do ENEM (Inep), os microdados do Censo "
        "Escolar da Educação Básica (Inep) e o Produto Interno Bruto dos Municípios (IBGE). Para viabilizar a manipulação dos arquivos volumosos, "
        "implementou-se um pipeline em Python que realiza a leitura e filtragem em fluxo contínuo (streaming por blocos de 100.000 linhas) "
        "diretamente a partir dos arquivos compactados (.zip), sem descompressão integral em disco."
    )
    story.append(Paragraph(p_met1, body_style))

    p_met2 = (
        "Foram aplicados três critérios estritos de seleção amostral: (1) participação no Distrito Federal (SG_UF_PROVA == 'DF'); (2) presença "
        "efetiva no segundo dia do certame (TP_PRESENCA_MT == 1) e obtenção de nota válida em Matemática; e (3) preenchimento das variáveis "
        "familiares essenciais no questionário socioeconômico. A amostra final resultou em N = 126.874 estudantes do Distrito Federal."
    )
    story.append(Paragraph(p_met2, body_style))

    story.append(Paragraph("3.2 Variáveis e Engenharia de Atributos", h2_style))
    p_met3 = (
        "A variável dependente (Y) do estudo é a Nota de Matemática e suas Tecnologias (NU_NOTA_MT). Os preditores (X) foram submetidos à engenharia "
        "de atributos: (a) a escolaridade do pai (Q001) e da mãe (Q002) foi convertida em anos de escolarização formais (0 a 18 anos), extraindo-se a "
        "Maior Escolaridade dos Pais (MAX_ESC_PAIS) como índice de capital cultural máximo do domicílio; (b) a renda familiar (Q006) foi convertida "
        "para valores monetários e transformada em escala logarítmica (LOG_RENDA) para corrigir assimetria distributiva; (c) foram criadas variáveis "
        "binárias para posse de computador (Q024) e internet (Q025); (d) a dependência administrativa foi codificada em dummies (Privada, Federal, Pública Distrital); "
        "e (e) incluíram-se controles de cor/raça (PPI = 1), sexo feminino (1 = F) e dummies dos anos de 2022 e 2023."
    )
    story.append(Paragraph(p_met3, body_style))

    story.append(Paragraph("3.3 Modelagem Estatística e Preditiva", h2_style))
    p_met4 = (
        "A estratégia analítica combina duas perspectivas complementares: (1) Regressão Linear Múltipla estimada por Mínimos Quadrados Ordinários (OLS), "
        "para inferência paramétrica e medição de efeitos marginais ceteris paribus; e (2) Random Forest Regressor supervisionado com 100 árvores de decisão "
        "e profundidade controlada (max_depth = 15). O conjunto amostral foi particionado em 70% para treinamento (N = 88.811) e 30% para teste (N = 38.063), "
        "com random_state = 42. A importância relativa de cada atributo foi computada via Mean Decrease in Impurity (MDI)."
    )
    story.append(Paragraph(p_met4, body_style))

    # -------------------------------------------------------------
    # 4.0 Resultados e Discussão
    # -------------------------------------------------------------
    story.append(Paragraph("4.0 Resultados e Discussão", h1_style))
    story.append(Paragraph("4.1 Análise Exploratória e Visual", h2_style))
    p_res1 = (
        "A Figura 1 apresenta a matriz de correlação de Pearson entre os fatores investigados e o rendimento em Matemática. A nota exibe forte correlação "
        "positiva com a Renda Familiar Mensal (r = 0,47), a Escolaridade do Pai (r = 0,38), a Escolaridade da Mãe (r = 0,36) e a Posse de Computador (r = 0,33), "
        "contrastando com correlação negativa com a condição PPI (r = -0,26)."
    )
    story.append(Paragraph(p_res1, body_style))

    # Inserção da Figura 1 (Heatmap)
    caminho_fig1 = Path("resultados/figuras/heatmap_correlacoes.png")
    if caminho_fig1.exists():
        story.append(Image(str(caminho_fig1), width=col_w, height=col_w * 0.78))
        story.append(Paragraph("Figura 1. Matriz de Correlação de Pearson: Variáveis Inep, IBGE e Nota de Matemática.", caption_style))

    p_res2 = (
        "Conforme previsto na formulação do projeto, a Figura 2 apresenta a mediana das notas em Matemática isolando as redes de ensino em cada "
        "nível de estudo dos genitores. Observa-se que, enquanto alunos da rede pública de pais sem instrução obtêm mediana de 435,5 pontos, "
        "alunos de pais com pós-graduação atingem 565 pontos. Contudo, em qualquer patamar de escolaridade familiar, a escola privada confere um "
        "salto marcante, atingindo mediana superior a 630 pontos nos estratos mais altos (mediana geral de 629,9 pontos versus 501,3 da rede distrital)."
    )
    story.append(Paragraph(p_res2, body_style))

    # Inserção da Figura 2 (Barras Rede)
    caminho_fig2 = Path("resultados/figuras/barras_mediana_escolaridade_rede.png")
    if caminho_fig2.exists():
        story.append(Image(str(caminho_fig2), width=col_w, height=col_w * 0.58))
        story.append(Paragraph("Figura 2. Mediana em Matemática por Maior Escolaridade dos Pais e Rede de Ensino no DF.", caption_style))

    p_res3 = (
        "A Figura 3 detalha a mediana das notas conforme a disponibilidade de computador no domicílio. Os participantes com computador alcançam "
        "mediana agregada de 575,5 pontos, contra 474,3 pontos dos que não dispõem do equipamento (diferencial expressivo de 101,2 pontos). "
        "Esse padrão ratifica que os bens tecnológicos domésticos ampliam a capacidade de fixação de conteúdos quantitativos e autoinstrução."
    )
    story.append(Paragraph(p_res3, body_style))

    # Inserção da Figura 3 (Barras Computador)
    caminho_fig3 = Path("resultados/figuras/barras_mediana_escolaridade_computador.png")
    if caminho_fig3.exists():
        story.append(Image(str(caminho_fig3), width=col_w, height=col_w * 0.58))
        story.append(Paragraph("Figura 3. Mediana em Matemática por Escolaridade dos Pais e Posse de Computador no DF.", caption_style))

    story.append(Paragraph("4.2 Efeitos Marginais: Regressão Linear Múltipla", h2_style))
    p_res4 = (
        "A Tabela 1 reúne os coeficientes da regressão linear múltipla (OLS). O modelo alcançou R² = 0,2784 com elevada significância (F = 4.079, p < 0,001), "
        "demonstrando que mais de um quarto da variabilidade das notas em Matemática decorre exclusivamente das variáveis estruturais e familiares inseridas."
    )
    story.append(Paragraph(p_res4, body_style))

    # Tabela 1: Regressão Linear
    dados_t1 = [
        [Paragraph("<b>Variável</b>", tbl_head), Paragraph("<b>Coef. (β)</b>", tbl_head), Paragraph("<b>Erro P.</b>", tbl_head), Paragraph("<b>t</b>", tbl_head), Paragraph("<b>p-valor</b>", tbl_head)],
        [Paragraph("Intercepto (β0)", tbl_cell), Paragraph("373,13", tbl_num), Paragraph("2,17", tbl_num), Paragraph("171,6", tbl_num), Paragraph("< 0,001", tbl_cell)],
        [Paragraph("Esc. Pai (anos)", tbl_cell), Paragraph("+4,08", tbl_num), Paragraph("0,09", tbl_num), Paragraph("46,2", tbl_num), Paragraph("< 0,001", tbl_cell)],
        [Paragraph("Esc. Mãe (anos)", tbl_cell), Paragraph("+3,65", tbl_num), Paragraph("0,09", tbl_num), Paragraph("38,9", tbl_num), Paragraph("< 0,001", tbl_cell)],
        [Paragraph("Log(Renda)", tbl_cell), Paragraph("+13,51", tbl_num), Paragraph("0,22", tbl_num), Paragraph("61,7", tbl_num), Paragraph("< 0,001", tbl_cell)],
        [Paragraph("Tem Computador", tbl_cell), Paragraph("+27,46", tbl_num), Paragraph("0,84", tbl_num), Paragraph("32,7", tbl_num), Paragraph("< 0,001", tbl_cell)],
        [Paragraph("Escola Privada", tbl_cell), Paragraph("+44,20", tbl_num), Paragraph("1,15", tbl_num), Paragraph("38,3", tbl_num), Paragraph("< 0,001", tbl_cell)],
        [Paragraph("Escola Federal", tbl_cell), Paragraph("+45,39", tbl_num), Paragraph("2,53", tbl_num), Paragraph("17,9", tbl_num), Paragraph("< 0,001", tbl_cell)],
        [Paragraph("Cor/Raça PPI", tbl_cell), Paragraph("-24,19", tbl_num), Paragraph("0,65", tbl_num), Paragraph("-37,1", tbl_num), Paragraph("< 0,001", tbl_cell)],
        [Paragraph("Sexo Feminino", tbl_cell), Paragraph("-32,85", tbl_num), Paragraph("0,64", tbl_num), Paragraph("-51,5", tbl_num), Paragraph("< 0,001", tbl_cell)],
    ]
    t1 = Table(dados_t1, colWidths=[col_w * 0.36, col_w * 0.17, col_w * 0.15, col_w * 0.14, col_w * 0.18])
    t1.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t1)
    story.append(Paragraph("Tabela 1. Coeficientes da Regressão Linear Múltipla OLS (R² = 0,2784, N = 126.874).", caption_style))

    p_res5 = (
        "Os coeficientes revelam que cada ano de estudo adicional do pai e da mãe agrega, respectivamente, +4,08 e +3,65 pontos líquidos à nota. "
        "Destaca-se o prêmio institucional da escola privada (+44,20 pontos) e federal (+45,39 pontos) frente à pública distrital, comprovando "
        "que o diferencial de desempenho persiste mesmo isolando a renda domiciliar."
    )
    story.append(Paragraph(p_res5, body_style))

    # Quebra de página para balancear a Página 4 com Random Forest, Conclusão e Referências
    story.append(PageBreak())

    story.append(Paragraph("4.3 Preditores Não Lineares e Ranking: Random Forest", h2_style))
    p_res6 = (
        "No conjunto de teste (30%), o Random Forest obteve R² = 0,2896, com erro absoluto médio (MAE) de 85,60 pontos. A Figura 4 expõe o ranking de "
        "importância de variáveis (MDI): a Renda Familiar Mensal lidera com 64,05% da força preditiva, seguida pela escolaridade paterna (8,22%) e "
        "materna (7,79%), somando 16,01% para o capital cultural. Dispositivos digitais, sexo e tipologia escolar complementam a capacidade preditiva."
    )
    story.append(Paragraph(p_res6, body_style))

    # Inserção da Figura 4 (Ranking RF)
    caminho_fig4 = Path("resultados/figuras/ranking_importancia_variaveis.png")
    if caminho_fig4.exists():
        story.append(Image(str(caminho_fig4), width=col_w, height=col_w * 0.62))
        story.append(Paragraph("Figura 4. Ranking de Importância de Variáveis via Random Forest Regressor (MDI).", caption_style))

    # Tabela 2: Médias por Subcategoria
    dados_t2 = [
        [Paragraph("<b>Dimensão / Subcategoria</b>", tbl_head), Paragraph("<b>N</b>", tbl_head), Paragraph("<b>Média</b>", tbl_head), Paragraph("<b>Mediana</b>", tbl_head)],
        [Paragraph("Rede Privada", tbl_cell), Paragraph("18.377", tbl_num), Paragraph("621,1", tbl_num), Paragraph("629,9", tbl_num)],
        [Paragraph("Rede Federal (IFB)", tbl_cell), Paragraph("2.207", tbl_num), Paragraph("601,0", tbl_num), Paragraph("600,5", tbl_num)],
        [Paragraph("Rede Pública Distrital", tbl_cell), Paragraph("26.063", tbl_num), Paragraph("511,6", tbl_num), Paragraph("501,3", tbl_num)],
        [Paragraph("Pais: Pós-graduação", tbl_cell), Paragraph("39.018", tbl_num), Paragraph("623,7", tbl_num), Paragraph("633,9", tbl_num)],
        [Paragraph("Pais: Ensino Superior", tbl_cell), Paragraph("27.731", tbl_num), Paragraph("586,2", tbl_num), Paragraph("588,1", tbl_num)],
        [Paragraph("Pais: Ensino Médio", tbl_cell), Paragraph("42.617", tbl_num), Paragraph("521,1", tbl_num), Paragraph("509,5", tbl_num)],
        [Paragraph("Pais: Sem estudo", tbl_cell), Paragraph("1.574", tbl_num), Paragraph("448,8", tbl_num), Paragraph("435,5", tbl_num)],
        [Paragraph("Possui Computador", tbl_cell), Paragraph("105.100", tbl_num), Paragraph("578,0", tbl_num), Paragraph("575,5", tbl_num)],
        [Paragraph("Não Possui Computador", tbl_cell), Paragraph("35.349", tbl_num), Paragraph("487,5", tbl_num), Paragraph("474,3", tbl_num)],
    ]
    t2 = Table(dados_t2, colWidths=[col_w * 0.46, col_w * 0.18, col_w * 0.18, col_w * 0.18])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t2)
    story.append(Paragraph("Tabela 2. Estatísticas Descritivas de Matemática por Subgrupo no DF (N = 126.874).", caption_style))

    # -------------------------------------------------------------
    # 5.0 Conclusão
    # -------------------------------------------------------------
    story.append(Paragraph("5.0 Conclusão", h1_style))
    p_concl1 = (
        "Este trabalho investigou as determinantes socioeconômicas e escolares do desempenho em Matemática no ENEM no Distrito Federal entre 2021 e 2023. "
        "A articulação entre regressão linear múltipla e Random Forest demonstrou que as condições familiares exercem influência decisiva: renda domiciliar "
        "e capital cultural dos genitores respondem por mais de 80% do poder preditivo das notas."
    )
    story.append(Paragraph(p_concl1, body_style))

    p_concl2 = (
        "Ao estabelecer diálogo com a literatura do Departamento de Ciência da Computação da UnB, em especial o trabalho de Silveira et al. (2022), "
        "esta pesquisa evidencia que as barreiras de rendimento e evasão observadas nas disciplinas introdutórias de computação (CS1) encontram raízes "
        "estruturais profundas já na educação básica. Políticas públicas de equalização de oportunidades devem priorizar a redução do abismo de infraestrutura "
        "entre escolas públicas e privadas, a garantia de acesso universal a dispositivos digitais e o fortalecimento de programas de nivelamento em ciências exatas."
    )
    story.append(Paragraph(p_concl2, body_style))

    # -------------------------------------------------------------
    # Referências Bibliográficas
    # -------------------------------------------------------------
    story.append(Paragraph("Referências", h1_style))
    refs = [
        "BOURDIEU, P.; PASSERON, J.-C. <b>La reproduction: éléments pour une théorie du système d'enseignement</b>. Paris: Éditions de Minuit, 1970.",
        "IBGE. <b>Produto Interno Bruto dos Municípios 2021–2023</b>. Rio de Janeiro: Instituto Brasileiro de Geografia e Estatística, 2024.",
        "INEP. <b>Microdados do Censo Escolar da Educação Básica (2021–2023)</b>. Brasília: Inep, 2024.",
        "INEP. <b>Microdados do Exame Nacional do Ensino Médio (2021–2023)</b>. Brasília: Inep, 2024.",
        "MORAES, B.; BELLUZZO, W. O diferencial de desempenho entre escolas públicas e privadas no Brasil. <b>Revista Brasileira de Economia</b>, v. 68, n. 4, p. 451–475, 2014.",
        "OECD. <b>PISA 2018 Results (Volume I): What Students Know and Can Do</b>. Paris: PISA, OECD Publishing, 2019.",
        "SILVEIRA, R. F.; HOLANDA, M.; RAMOS, G. N. Analysis of Student Performance and Social-economic Data in Introductory Computer Science Courses at the University of Brasília. In: <b>2022 IEEE Frontiers in Education Conference (FIE)</b>. Uppsala: IEEE, 2022. p. 1–8."
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle("Ref", fontName="Times-Roman", fontSize=7, leading=9.2, alignment=TA_JUSTIFY, spaceAfter=2.5)))

    doc.build(story)
    print(f"\n[SUCESSO TOTAL] Artigo Completo em PDF gerado em: {caminho_pdf.resolve()}")
    return caminho_pdf

if __name__ == "__main__":
    gerar_artigo()
