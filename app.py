import streamlit as st
import pandas as pd
from datetime import datetime
import time
import os

# ----------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA
# ----------------------------------------------------
st.set_page_config(
    page_title="Tutor de Matemática e Cidadania - EPDRG",
    page_icon="🎓",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "Logo.rm.png")
CSV_PATH = os.path.join(BASE_DIR, "respostas_alunos.csv")

# ----------------------------------------------------
# 2. SISTEMA DE TELEMETRIA E REGISTO DOCENTE
# ----------------------------------------------------
def guardar_registo(nome, turma, tarefa, data_inicio, data_reinicio, ex_id, pergunta, resposta, correta, tentativas, tempo_segundos, tipo_evento="Resposta"):
    dados = {
        "Data_Hora": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Data_Inicio_Tarefa": [data_inicio],
        "Data_Reinicio_Sessao": [data_reinicio if data_reinicio else "Primeira Sessão"],
        "Aluno": [nome],
        "Turma": [turma],
        "Tarefa": [tarefa],
        "Exercicio": [ex_id],
        "Tipo_Evento": [tipo_evento],
        "Pergunta": [pergunta],
        "Resposta_Dada": [str(resposta)],
        "Resultado": ["Correta" if correta else ("Incorreta" if tipo_evento == "Resposta" else "-")],
        "Tentativas": [tentativas],
        "Tempo_Segundos": [round(tempo_segundos, 1)]
    }
    df_novo = pd.DataFrame(dados)
    if not os.path.exists(CSV_PATH):
        df_novo.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
    else:
        df_novo.to_csv(CSV_PATH, mode="a", header=False, index=False, encoding="utf-8-sig")

# ----------------------------------------------------
# 3. BASE DE DADOS INTEGRAL DAS 6 TAREFAS
# ----------------------------------------------------
DADOS_TAREFAS = {
    "Tarefa 1: Maioria Simples e Maioria Absoluta": {
        "resumo_teorico": """
        ### 1. Resumo Teórico
        * **Eleições Presidenciais:** Periodicidade de 5 em 5 anos; sufrágio direto e universal; mandato de 5 anos; pode haver segunda volta.
        * **Eleições Legislativas:** Máximo de 4 em 4 anos; representação proporcional pelo Método de Hondt.
        * **Tipos de Votos:**
          * **Votos em branco:** boletins sem qualquer marcação.
          * **Votos nulos:** boletins com rasuras ou marcas que não identificam claramente uma opção.
          * **Votos validamente expressos:** votos que determinam os resultados:
            $$\\text{Votos Válidos} = \\text{Votantes} - (\\text{Votos em Branco} + \\text{Votos Nulos})$$
        * **Taxa de Abstenção:** Percentagem de eleitores inscritos que não votaram:
          $$\\text{Taxa de Abstenção} = \\frac{\\text{Inscritos} - \\text{Votantes}}{\\text{Inscritos}} \\times 100$$
        * **Maioria Simples (Relativa):** Vence o candidato/opção com maior número de votos.
        * **Maioria Absoluta:** Exige mais de 50% dos votos validamente expressos (metade mais 1 em números inteiros). Se ninguém atingir na 1.ª volta, realiza-se uma 2.ª volta entre os dois mais votados.
        """,
        "exemplo_aplicacao": """
        ### 2. Exemplo de Aplicação Resolvido (Presidenciais de 2021)
        * **Dados Oficiais:** Inscritos: $10\\,864\\,327$ | Votantes: $4\\,262\\,672$ ($39,24\%$) | Brancos: $47\\,055$ | Nulos: $40\\,026$.
        * **Votos Válidos:** $4\\,262\\,672 - (47\\,055 + 40\\,026) = 4\\,175\\,591$ votos.
        * **Abstenção:** $10\\,864\\,327 - 4\\,262\\,672 = 6\\,601\\,655 \\longrightarrow \\frac{6\\,601\\,655}{10\\,864\\,327} \\times 100 \\approx 60,76\%$.
        * **Decisão:** Marcelo Rebelo de Sousa obteve $60,70\%$ dos votos válidos ($> 50\%$), sendo eleito à primeira volta por maioria absoluta.
        """,
        "exercicios": [
            {
                "id": "1.1.1",
                "titulo": "Exercício 1.1.1 — 1.ª Eleição Presidencial da Democracia (1976)",
                "enunciado": "> **Dados Oficiais (1976):** Votantes: 4 881 125 | Brancos: 20 253 | Nulos: 43 242 | Inscritos: 6 467 480",
                "pergunta": "Determine o número de votos validamente expressos:",
                "tipo": "int",
                "resposta_correta": 4817630,
                "tolerancia": 0,
                "dica": "Votos Válidos = Votantes - Brancos - Nulos (4 881 125 - 20 253 - 43 242)."
            },
            {
                "id": "1.1.2",
                "titulo": "Exercício 1.1.2 — Taxa de Abstenção em 1976",
                "enunciado": "> Inscritos: 6 467 480 | Votantes: 4 881 125",
                "pergunta": "Determine a percentagem de abstenção, arredondada às décimas (ex: 24.5):",
                "tipo": "float",
                "resposta_correta": 24.5,
                "tolerancia": 0.2,
                "dica": "Calcula a abstenção (6 467 480 - 4 881 125 = 1 586 355), divide pelos inscritos e multiplica por 100."
            },
            {
                "id": "1.1.3",
                "titulo": "Exercício 1.1.3 — Percentagem de Ramalho Eanes",
                "enunciado": "> António Ramalho Eanes obteve 2 967 137 votos num total de 4 817 630 votos válidos.",
                "pergunta": "Determine a percentagem de votos obtida por este candidato, arredondada às décimas:",
                "tipo": "float",
                "resposta_correta": 61.6,
                "tolerancia": 0.2,
                "dica": "Divide 2 967 137 por 4 817 630 e multiplica por 100."
            },
            {
                "id": "1.1.4",
                "titulo": "Exercício 1.1.4 — Presidente Eleito em 1976",
                "enunciado": "> Para ser eleito Presidente na 1.ª volta é necessário obter mais de 50% dos votos válidos.",
                "pergunta": "Identifique o candidato eleito Presidente da República em 1976:",
                "tipo": "choice",
                "opcoes": ["Selecione...", "António Ramalho Eanes", "José Pinheiro de Azevedo", "Otávio Rodrigues Pato", "Otelo Saraiva de Carvalho"],
                "resposta_correta": "António Ramalho Eanes",
                "dica": "António Ramalho Eanes superou a barreira dos 50% com 61,6% dos votos válidos."
            },
            {
                "id": "1.2.1",
                "titulo": "Exercício 1.2.1 — Eleição de Delegado no Curso de Ação Educativa",
                "enunciado": "> Turma com 23 alunos. No dia da eleição faltou a Maria (22 votantes). Resultados: João (5), Catarina (6), Francisca (10), Branco (1). Votos válidos = 21.",
                "pergunta": "Calcula a percentagem de votos válidos face aos votantes (arredondada às centésimas, ex: 95.45):",
                "tipo": "float",
                "resposta_correta": 95.45,
                "tolerancia": 0.05,
                "dica": "Divide os votos válidos (21) pelo total de votantes (22) e multiplica por 100."
            },
            {
                "id": "1.2.2",
                "titulo": "Exercício 1.2.2 — Eleito por Maioria Simples",
                "enunciado": "> Resultados: João: 5 votos | Catarina: 6 votos | Francisca: 10 votos.",
                "pergunta": "Qual teria sido o aluno eleito se fosse aplicado o método de maioria simples?",
                "tipo": "choice",
                "opcoes": ["Selecione...", "João", "Catarina", "Francisca"],
                "resposta_correta": "Francisca",
                "dica": "Por maioria simples vence a opção que tiver o maior número de votos (Francisca com 10 votos)."
            },
            {
                "id": "1.2.3",
                "titulo": "Exercício 1.2.3 — Mínimo para Maioria Absoluta",
                "enunciado": "> Votos válidos expressos: 21 votos.",
                "pergunta": "Indica o número mínimo de votos inteiros que um aluno teria de obter para vencer por maioria absoluta:",
                "tipo": "int",
                "resposta_correta": 11,
                "tolerancia": 0,
                "dica": "Metade de 21 é 10,5. O menor número inteiro estritamente superior a 50% é 11."
            },
            {
                "id": "1.2.4",
                "titulo": "Exercício 1.2.4 — Desfecho da Eleição",
                "enunciado": "> Mínimo para maioria absoluta: 11 votos. Francisca obteve 10 votos e Catarina obteve 6 votos.",
                "pergunta": "Algum aluno venceu por maioria absoluta?",
                "tipo": "choice",
                "opcoes": [
                    "Selecione...",
                    "Não, nenhum aluno atingiu os 11 votos necessários (vai a 2.ª volta entre Francisca e Catarina)",
                    "Sim, a Francisca venceu logo na 1.ª volta",
                    "Sim, a Catarina e o João empataram"
                ],
                "resposta_correta": "Não, nenhum aluno atingiu os 11 votos necessários (vai a 2.ª volta entre Francisca e Catarina)",
                "dica": "Como a mais votada tem 10 votos (< 11), é obrigatório realizar 2.ª volta entre as duas mais votadas."
            },
            {
                "id": "1.3.1",
                "titulo": "Exercício 1.3.1 — Empresa de Marketing: Taxa de Abstenção",
                "enunciado": "> 345 funcionários. Votantes: 149 (Madeira) + 87 (Barcelona) + 59 (Paris) + 11 (Nulos) + 4 (Brancos) = 310 votantes.",
                "pergunta": "Qual foi a percentagem de abstenção nesta votação? (Arredondada às décimas, ex: 10.1):",
                "tipo": "float",
                "resposta_correta": 10.1,
                "tolerancia": 0.15,
                "dica": "Abstenção = 345 - 310 = 35. Taxa = (35 / 345) * 100."
            },
            {
                "id": "1.3.2",
                "titulo": "Exercício 1.3.2 — Percentagem de Votos na Madeira",
                "enunciado": "> Destino Madeira obteve 149 votos num total de 295 votos válidos.",
                "pergunta": "Determina a percentagem de votos da Madeira (arredondada às centésimas, ex: 50.51):",
                "tipo": "float",
                "resposta_correta": 50.51,
                "tolerancia": 0.05,
                "dica": "Divide 149 por 295 e multiplica por 100."
            },
            {
                "id": "1.3.3",
                "titulo": "Exercício 1.3.3 — Vencedor na Empresa de Marketing",
                "enunciado": "> Madeira obteve 149 votos (50,51%), Barcelona 87 votos e Paris 59 votos.",
                "pergunta": "O destino vencedor seria o mesmo caso o método aplicado fosse o de maioria absoluta?",
                "tipo": "choice",
                "opcoes": [
                    "Selecione...",
                    "Sim, porque a Madeira obteve 50,51% dos votos válidos (mais de metade)",
                    "Não, porque seria necessária uma 2.ª volta com Barcelona",
                    "Não, porque não participaram todos os funcionários"
                ],
                "resposta_correta": "Sim, porque a Madeira obteve 50,51% dos votos válidos (mais de metade)",
                "dica": "Com 50,51% a Madeira superou metade dos votos válidos logo na primeira contagem."
            },
            {
                "id": "1.4.1",
                "titulo": "Exercício 1.4.1 — Evento do Curso de Desporto",
                "enunciado": "> Votantes: 2430 | Votos válidos: 1872 (Zumba: 893, Body Combat: 478, Ioga: 294, Defesa Pessoal: 113, Spinning: 94).",
                "pergunta": "Qual foi a percentagem de votos válidos face aos votantes? (Arredondada às unidades inteiras, ex: 77):",
                "tipo": "int",
                "resposta_correta": 77,
                "tolerancia": 0,
                "dica": "(1872 / 2430) * 100 = 77,037% -> 77%."
            },
            {
                "id": "1.4.2",
                "titulo": "Exercício 1.4.2 — Desfecho por Maioria Absoluta no Desporto",
                "enunciado": "> Votos válidos: 1872. Mínimo para maioria absoluta = 937 votos. Zumba obteve 893 e Body Combat 478.",
                "pergunta": "Aplicando o método de maioria absoluta, qual o desfecho da eleição?",
                "tipo": "choice",
                "opcoes": [
                    "Selecione...",
                    "Nenhuma modalidade venceu na 1.ª volta; avançam para a 2.ª volta o Zumba e o Body Combat",
                    "O Zumba venceu logo na 1.ª volta por ter mais votos",
                    "Avançam para a 2.ª volta o Zumba e o Ioga"
                ],
                "resposta_correta": "Nenhuma modalidade venceu na 1.ª volta; avançam para a 2.ª volta o Zumba e o Body Combat",
                "dica": "O Zumba teve 893 votos (< 937), pelo que as duas modalidades mais votadas disputam a 2.ª volta."
            },
            {
                "id": "1.5.1",
                "titulo": "Exercício 1.5.1 — Eleição no 10.º TGEI",
                "enunciado": "> Turma com 27 alunos, faltaram 2 (25 votantes). 20 votos nos candidatos: Rodrigo (8), Ricardo (6), Letícia (3), Ângelo (3). Maioria absoluta exige 11 votos.",
                "pergunta": "Considerando que Rodrigo mantém os seus 8 votos, quantos votos no mínimo o Ricardo tem de captar na 2.ª volta para vencer?",
                "tipo": "int",
                "resposta_correta": 3,
                "tolerancia": 0,
                "dica": "O Ricardo tem 6 votos. Para ultrapassar os 8 votos do Rodrigo precisa de alcançar no mínimo 9 votos (6 + 3 = 9)."
            }
        ]
    },

    "Tarefa 2: Método da Borda": {
        "resumo_teorico": """
        ### 1. Resumo Teórico
        * Numa eleição com $N$ opções em confronto:
          * 1.ª preferência recebe **$N$ pontos**;
          * 2.ª preferência recebe **$N - 1$ pontos**;
          * ... e a última preferência recebe **1 ponto**.
        * Multiplica-se o total de votos de cada coluna pelos respetivos pontos e somam-se as parcelas por cada opção.
        * Vence quem acumular o **maior total de pontos**.
        """,
        "exemplo_aplicacao": """
        ### 2. Exemplo de Aplicação Resolvido (Eleição da Mascote da Escola)
        * **Candidatos (5 opções):** Girafa (G), Panda (P), Tigre (T), Crocodilo (C), Urso (U).
        * **Pontos:** 1.ª (5 pts), 2.ª (4 pts), 3.ª (3 pts), 4.ª (2 pts), 5.ª (1 pt).
        * **Pontuação Final Acumulada:**
          * Panda: $5\\times 132 + 4\\times 145 + 2\\times 80 + 2\\times 102 + 2\\times 125 = 1854\\text{ pontos}$
          * Tigre: $5\\times 145 + 4\\times 102 + 3\\times 125 + 2\\times 132 + 1\\times 80 = 1852\\text{ pontos}$
          * Girafa: $1844\\text{ pts}$ | Urso: $1641\\text{ pts}$ | Crocodilo: $1569\\text{ pts}$.
        * **Vencedor:** Panda (1854 pontos).
        """,
        "exercicios": [
            {
                "id": "Borda.1.1",
                "titulo": "Exercício 1.1 — Representante no Projeto de Mandarim",
                "enunciado": (
                    "> Candidatos: Bernardo (B), Célia (C), Manuel (M), Ricardo (R). 47 votos validados:\n\n"
                    "> | Preferências | 14 votos | 21 votos | 9 votos | 3 votos |\n"
                    "> | :--- | :---: | :---: | :---: | :---: |\n"
                    "> | **1.ª (4 pts)** | B | R | M | C |\n"
                    "> | **2.ª (3 pts)** | C | B | R | M |\n"
                    "> | **3.ª (2 pts)** | M | C | B | R |\n"
                    "> | **4.ª (1 pt)**  | R | M | C | B |"
                ),
                "pergunta": "Pelo método de Borda, qual aluno obteve mais pontos e vai representar a escola?",
                "tipo": "choice",
                "opcoes": ["Selecione...", "Bernardo (B)", "Célia (C)", "Manuel (M)", "Ricardo (R)"],
                "resposta_correta": "Bernardo (B)",
                "dica": "Pontuações: Bernardo = 140 pts, Ricardo = 131 pts, Célia = 105 pts, Manuel = 94 pts."
            },
            {
                "id": "Borda.1.2",
                "titulo": "Exercício 1.2 — Comparação com a Maioria Simples",
                "enunciado": "> Votos de 1.ª preferência: Ricardo (21), Bernardo (14), Manuel (9), Célia (3).",
                "pergunta": "Considerando apenas as primeiras preferências por maioria simples, o representante seria o mesmo?",
                "tipo": "choice",
                "opcoes": [
                    "Selecione...",
                    "Não seria o mesmo; por maioria simples venceria o Ricardo com 21 votos",
                    "Sim, continuaria a vencer o Bernardo",
                    "Não seria o mesmo; venceria o Manuel com 9 votos"
                ],
                "resposta_correta": "Não seria o mesmo; por maioria simples venceria o Ricardo com 21 votos",
                "dica": "Na 1.ª linha da tabela o Ricardo tem 21 votos, enquanto o Bernardo tem 14."
            },
            {
                "id": "Borda.1.3",
                "titulo": "Exercício 1.3 — Eleição no Modelo Presidencial Português",
                "enunciado": "> Universo de 47 votos validados. Ricardo obteve 21 votos de 1.ª escolha e Bernardo obteve 14.",
                "pergunta": "Se fosse utilizado o método presidencial português (maioria absoluta), seria necessária 2.ª volta?",
                "tipo": "choice",
                "opcoes": [
                    "Selecione...",
                    "Sim, necessária 2.ª volta entre o Ricardo (21 votos) e o Bernardo (14 votos)",
                    "Não seria necessária 2.ª volta, pois o Ricardo venceu a 1.ª volta",
                    "Sim, necessária 2.ª volta entre todos os quatro candidatos"
                ],
                "resposta_correta": "Sim, necessária 2.ª volta entre o Ricardo (21 votos) e o Bernardo (14 votos)",
                "dica": "Maioria absoluta em 47 votos exige pelo menos 24 votos. Como ninguém atingiu, os dois primeiros vão a 2.ª volta."
            },
            {
                "id": "Borda.2.1",
                "titulo": "Exercício 2.1 — Novo Prato no Restaurante (Total de Clientes)",
                "enunciado": "> Pratos: Carne de porco (C), Polvo (P), Bacalhau (B). Votação: Coluna 1 (12 votos), Coluna 2 (5 votos), Coluna 3 (9 votos).",
                "pergunta": "Quantos clientes estavam no restaurante?",
                "tipo": "int",
                "resposta_correta": 26,
                "tolerancia": 0,
                "dica": "Soma todos os votos das três colunas: 12 + 5 + 9 = 26."
            },
            {
                "id": "Borda.2.2",
                "titulo": "Exercício 2.2 — Prato Escolhido pelo Método de Borda",
                "enunciado": "> 3 pratos em disputa (1.ª = 3 pts, 2.ª = 2 pts, 3.ª = 1 pt).",
                "pergunta": "Pelo método de Borda, qual foi o prato escolhido?",
                "tipo": "choice",
                "opcoes": ["Selecione...", "Bacalhau à Gomes de Sá (B)", "Carne de porco com amêijoas (C)", "Polvo à Lagareiro (P)"],
                "resposta_correta": "Bacalhau à Gomes de Sá (B)",
                "dica": "Pontuações: Bacalhau = 56 pts, Carne de porco = 55 pts, Polvo = 45 pts."
            },
            {
                "id": "Borda.3.1",
                "titulo": "Exercício 3 — Escolha do Cartaz sobre Redes Sociais",
                "enunciado": "> 28 alunos de Comunicação Digital votaram nos cartazes A, B e C: Coluna 1 (12 votos), Coluna 2 (6 votos), Coluna 3 (10 votos).",
                "pergunta": "Pelo método de Borda, qual foi o cartaz escolhido?",
                "tipo": "choice",
                "opcoes": ["Selecione...", "Cartaz A", "Cartaz B", "Cartaz C"],
                "resposta_correta": "Cartaz C",
                "dica": "Pontos: Cartaz C = 62 pts, Cartaz A = 58 pts, Cartaz B = 48 pts."
            },
            {
                "id": "Borda.4.1",
                "titulo": "Exercício 4 — Curso Preferido pelos Alunos do 9.º Ano",
                "enunciado": "> 89 alunos votaram nos cursos AE, CS e CP: Coluna 1 (23 votos), Coluna 2 (41 votos), Coluna 3 (25 votos).",
                "pergunta": "Pela aplicação do método de Borda, qual foi o curso preferido?",
                "tipo": "choice",
                "opcoes": ["Selecione...", "Técnico de Cozinha/Pastelaria (CP)", "Técnico de Comunicação e Serviço Digital (CS)", "Técnico de Ação Educativa (AE)"],
                "resposta_correta": "Técnico de Cozinha/Pastelaria (CP)",
                "dica": "Pontuações: CP = 196 pts, CS = 176 pts, AE = 162 pts."
            },
            {
                "id": "Borda.5.1",
                "titulo": "Exercício 5.1 — Jantar da Empresa (3 Restaurantes)",
                "enunciado": "> Cantina da Diana (CD), Churrasco do Tio Marco (CM), Sabores da Avó (SA). Votos: 8, 12 e 11.",
                "pergunta": "Aplicando o método de Borda, qual é o restaurante eleito?",
                "tipo": "choice",
                "opcoes": ["Selecione...", "Cantina da Diana (CD)", "Churrasco do Tio Marco (CM)", "Sabores da Avó (SA)"],
                "resposta_correta": "Cantina da Diana (CD)",
                "dica": "Pontuações: CD = 65 pts, CM = 63 pts, SA = 58 pts."
            },
            {
                "id": "Borda.5.2",
                "titulo": "Exercício 5.2 — Entrada do Restaurante 'The Best'",
                "enunciado": "> Nova votação com 4 restaurantes (4, 3, 2 e 1 pontos): Coluna 1 (4 votos), Coluna 2 (10 votos), Coluna 3 (9 votos), Coluna 4 (8 votos).",
                "pergunta": "Aplicando o método de Borda, o restaurante The Best (TB) foi o eleito?",
                "tipo": "choice",
                "opcoes": [
                    "Selecione...",
                    "Sim, o restaurante The Best (TB) foi o eleito com 95 pontos",
                    "Não, o eleito foi o Sabores da Avó (SA) com 74 pontos",
                    "Não, o eleito foi o Churrasco do Tio Marco (CM) com 72 pontos"
                ],
                "resposta_correta": "Sim, o restaurante The Best (TB) foi o eleito com 95 pontos",
                "dica": "TB totaliza: 4(1) + 10(4) + 9(3) + 8(3) = 4 + 40 + 27 + 24 = 95 pontos, superando todos os concorrentes."
            }
        ]
    },

    "Tarefa 3: Método de Hondt e Sainte-Laguë": {
        "resumo_teorico": """
        ### 1. Resumo Teórico
        * **Método de Hondt:**
          * Divisões sucessivas pelos números inteiros: **1, 2, 3, 4, 5, 6, 7...**
          * Favorece as listas mais votadas e fomenta a agregação/maiorias.
        * **Método de Sainte-Laguë:**
          * Divisões sucessivas apenas por números ímpares: **1, 3, 5, 7, 9...**
          * Favorece as listas de menor dimensão, promovendo representatividade ampla.
        """,
        "exemplo_aplicacao": """
        ### 2. Exemplo de Aplicação Resolvido (Hondt vs. Sainte-Laguë em Faro)
        * **5 alunos a distribuir por 4 escolas:** Sotavento (13), Barlavento (9), Ria Formosa (7), Barrocal (4).
        * **Por Hondt (/1, /2, /3):** Maiores quocientes: 13, 9, 7, 6.5 (Sotavento), 4.5 (Barlavento).
          * Sotavento: **2** | Barlavento: **2** | Ria Formosa: **1** | Barrocal: **0** (menor escola sem representante).
        * **Por Sainte-Laguë (/1, /3, /5):** Maiores quocientes: 13, 9, 7, 4.33 (Sotavento), 4 (Barrocal /1).
          * Sotavento: **2** | Barlavento: **1** | Ria Formosa: **1** | Barrocal: **1** (favoreceu a escola menos votada).
        """,
        "exercicios": [
            {
                "id": "Hondt.1.1",
                "titulo": "Exercício 1.1 — Prémios nas Modalidades Desportivas",
                "enunciado": "> 5 prémios por Hondt: Voleibol (211), Futebol (145), Basquetebol (103), Dança (78).",
                "pergunta": "Qual foi a modalidade com maior número de prémios atribuído?",
                "tipo": "choice",
                "opcoes": [
                    "Selecione...",
                    "Futebol e Voleibol (empatadas com 2 prémios cada)",
                    "Voleibol isolado com 3 prémios",
                    "Futebol isolado com 2 prémios"
                ],
                "resposta_correta": "Futebol e Voleibol (empatadas com 2 prémios cada)",
                "dica": "Quocientes apurados: 211 (Vol), 145 (Fut), 105.5 (Vol), 103 (Basq), 78 (Dança) ou 72.5 (Fut). Voleibol e Futebol asseguraram 2 prémios."
            },
            {
                "id": "Hondt.2.1",
                "titulo": "Exercício 2.1 — Bicicletas no Pré-Escolar (Sala Vermelha)",
                "enunciado": "> 6 bicicletas por Hondt: Vermelha (26), Azul (22), Amarela (18), Verde (15).",
                "pergunta": "Quantas bicicletas foram atribuídas à Sala Vermelha?",
                "tipo": "int",
                "resposta_correta": 2,
                "tolerancia": 0,
                "dica": "A sala Vermelha garante o 1.º quociente (26) e o 5.º quociente (13)."
            },
            {
                "id": "Hondt.2.2",
                "titulo": "Exercício 2.2 — Bicicletas no Pré-Escolar (Sala Azul)",
                "enunciado": "> Divisores de Hondt: 22 / 1 = 22 e 22 / 2 = 11.",
                "pergunta": "Quantas bicicletas foram atribuídas à Sala Azul?",
                "tipo": "int",
                "resposta_correta": 2,
                "tolerancia": 0,
                "dica": "A sala Azul garante o 2.º quociente (22) e o 6.º quociente (11)."
            },
            {
                "id": "Hondt.3.1",
                "titulo": "Exercício 3 — Televisões nos Lares de Idosos",
                "enunciado": "> 4 televisões por Hondt: Lar Saudável (34), Lar Felicidade (25), Lar Amizade (17).",
                "pergunta": "Quantas televisões recebeu o Lar Saudável?",
                "tipo": "int",
                "resposta_correta": 2,
                "tolerancia": 0,
                "dica": "O Lar Saudável garante o 1.º quociente (34) e empata no 3.º/4.º lugar com 17 (34 / 2)."
            },
            {
                "id": "Hondt.4.1",
                "titulo": "Exercício 4 — Cabazes Alimentares de Solidariedade",
                "enunciado": "> 5 cabazes por Hondt: Instituição C (90 utentes), Instituição A (76 utentes), Instituição B (48 utentes).",
                "pergunta": "Como ficaram distribuídos os 5 cabazes alimentares pelas instituições?",
                "tipo": "choice",
                "opcoes": [
                    "Selecione...",
                    "Instituição C: 2 cabazes; Instituição A: 2 cabazes; Instituição B: 1 cabaz",
                    "Instituição C: 3 cabazes; Instituição A: 1 cabaz; Instituição B: 1 cabaz",
                    "Instituição C: 2 cabazes; Instituição A: 1 cabaz; Instituição B: 2 cabazes"
                ],
                "resposta_correta": "Instituição C: 2 cabazes; Instituição A: 2 cabazes; Instituição B: 1 cabaz",
                "dica": "Quocientes: 90 (C), 76 (A), 48 (B), 45 (C /2) e 38 (A /2)."
            },
            {
                "id": "Hondt.5.1",
                "titulo": "Exercício 5 — Contentores de Óleos na Vila Piscatória",
                "enunciado": "> 6 contentores por Hondt: Conserva (4235), Restaurantes (1240), Zona Ind. (856), Mercado (745).",
                "pergunta": "Qual foi o número de contentores colocados perto do Mercado do Peixe?",
                "tipo": "int",
                "resposta_correta": 0,
                "tolerancia": 0,
                "dica": "Os 6 contentores foram atribuídos à Conserva (4), Restaurantes (1) e Zona Industrial (1). Nenhum ao Mercado."
            },
            {
                "id": "SaintLague.6.1",
                "titulo": "Exercício 6 — Sainte-Laguë vs. Hondt (Bicicletas)",
                "enunciado": "> Um aluno afirmou que se aplicasse Sainte-Laguë (/1 e /3) às 6 bicicletas, a distribuição pelas salas seria diferente.",
                "pergunta": "O aluno tem razão?",
                "tipo": "choice",
                "opcoes": [
                    "Selecione...",
                    "Não tem razão; a distribuição mantém-se idêntica (Vermelha: 2, Azul: 2, Amarela: 1, Verde: 1)",
                    "Sim, tem razão; a sala Verde ganharia 2 bicicletas",
                    "Sim, tem razão; a sala Vermelha ganharia 3 bicicletas"
                ],
                "resposta_correta": "Não tem razão; a distribuição mantém-se idêntica (Vermelha: 2, Azul: 2, Amarela: 1, Verde: 1)",
                "dica": "Calculando por divisores ímpares (1 e 3), os 6 maiores quocientes continuam a dar a mesma atribuição."
            },
            {
                "id": "SaintLague.8.1",
                "titulo": "Exercício 8 — Análise Crítica (João vs. Matilde no Desporto)",
                "enunciado": "> Matilde afirmou que por Sainte-Laguë o Futebol ganhava mais um prémio. O João afirmou que ficaria tudo igual.",
                "pergunta": "Quem tem razão?",
                "tipo": "choice",
                "opcoes": [
                    "Selecione...",
                    "Nenhum tem razão: por Sainte-Laguë o Futebol perde um prémio (fica com 1) e a Dança ganha 1 prémio",
                    "A Matilde tem razão, o Futebol fica com 3 prémios",
                    "O João tem razão, não há alteração"
                ],
                "resposta_correta": "Nenhum tem razão: por Sainte-Laguë o Futebol perde um prémio (fica com 1) e a Dança ganha 1 prémio",
                "dica": "Por Sainte-Laguë (/1 e /3): Voleibol: 2, Basquetebol: 1, Futebol: 1 e Dança: 1."
            }
        ]
    },

    "Tarefa 4: Matemática nos Salários": {
        "resumo_teorico": """
        ### 1. Resumo Teórico
        * **Segurança Social (SS):** Taxa de $11\%$ aplicada sobre a remuneração bruta: $\\text{SS} = \\text{Salário Bruto} \\times 0,11$.
        * **Retenção na Fonte de IRS:** Retenção mensal apurada sobre o salário bruto conforme tabelas legais.
        * **Subsídio de Refeição:** Isento de impostos até $6,00\\text{ €/dia}$ inclusive: $\\text{Dias Trabalhados} \\times \\text{Valor Diário}$.
        * **Valor a Receber:**
          $$\\text{Salário Líquido Base} = \\text{Salário Bruto} - \\text{SS} - \\text{IRS}$$
          $$\\text{Total a Receber} = \\text{Salário Líquido Base} + \\text{Subsídio de Refeição}$$
        """,
        "exemplo_aplicacao": """
        ### 2. Exemplo de Aplicação Resolvido (Catarina — Abril de 2023)
        * **Dados:** Salário bruto: $1256,20\\text{ €}$ | Casada 2 titulares, 1 dependente (Taxa IRS Tabela III = $12,3\%$).
        * **Subsídio:** 20 dias úteis a $5,20\\text{ €/dia} = 104,00\\text{ €}$.
        * **Descontos:** SS ($11\%$) = $138,18\\text{ €}$ | IRS ($12,3\%$) = $154,51\\text{ €}$.
        * **Cálculo Líquido:** $1256,20 - 138,18 - 154,51 = 963,51\\text{ €}$.
        * **Total no Final do Mês:** $963,51 + 104,00 = 1067,51\\text{ €}$ (ou $1067,58\\text{ €}$ com dízimas completas).
        """,
        "exercicios": [
            {
                "id": "Salarios.1",
                "titulo": "Exercício 1 — O Caso do Mateus (Açores)",
                "enunciado": "> Salário bruto: 1956,40 €. SS: 11%. Retenção IRS: 14,6%. Trabalhou 22 dias úteis a 5,80 €/dia de refeição.",
                "pergunta": "Quanto recebeu no total em setembro de 2022? (Arredonda às centésimas):",
                "tipo": "float",
                "resposta_correta": 1583.17,
                "tolerancia": 0.5,
                "dica": "Líquido base = 1956.40 - 215.20 (SS) - 285.63 (IRS) = 1455.57 €. Soma o subsídio (22 * 5.80 = 127.60 €) = 1583.17 €."
            },
            {
                "id": "Salarios.2.1",
                "titulo": "Exercício 2.1 — Carlos em Fevereiro de 2010",
                "enunciado": "> Salário bruto: 845 €. SS: 11% (92,95 €). Taxa IRS: 5,67% (47,91 €). 21 dias a 5,20 €/dia de almoço (109,20 €).",
                "pergunta": "Qual foi o valor líquido total recebido em fevereiro de 2010?",
                "tipo": "float",
                "resposta_correta": 813.34,
                "tolerancia": 0.5,
                "dica": "Faz: 845 - 92.95 - 47.91 + 109.20 = 813.34 €."
            },
            {
                "id": "Salarios.2.2",
                "titulo": "Exercício 2.2 — Carlos em Fevereiro de 2023",
                "enunciado": "> Salário bruto: 975 €. SS: 11% (107,25 €). Taxa IRS: 5% (48,75 €). 20 dias a 5,90 €/dia de almoço (118,00 €).",
                "pergunta": "Qual foi o valor líquido total recebido em fevereiro de 2023?",
                "tipo": "float",
                "resposta_correta": 937.00,
                "tolerancia": 0.5,
                "dica": "Faz: 975 - 107.25 - 48.75 + 118.00 = 937.00 €."
            },
            {
                "id": "Salarios.3",
                "titulo": "Exercício 3 — Mariana (Junta de Freguesia)",
                "enunciado": "> Salário bruto: 1700 €. SS: 11% (187,00 €). Escalão com taxa IRS de 16,1% (273,70 €). 22 dias a 5,20 € de refeição (114,40 €).",
                "pergunta": "Determina o valor que a Mariana vai receber no próximo mês:",
                "tipo": "float",
                "resposta_correta": 1353.70,
                "tolerancia": 0.5,
                "dica": "SL = 1700 + 114.40 - 187.00 - 273.70 = 1353.70 €."
            },
            {
                "id": "Salarios.4",
                "titulo": "Exercício 4 — Catarina após a Maternidade (Setembro 2023)",
                "enunciado": "> Salário aumentou 1,3% (1272,53 €). 2 dependentes (Taxa IRS 11,4% = 145,07 €). SS 11% (139,98 €). 19 dias a 6,00 €/dia (114,00 €).",
                "pergunta": "Quanto recebeu a Catarina no final de setembro de 2023?",
                "tipo": "float",
                "resposta_correta": 1101.48,
                "tolerancia": 1.0,
                "dica": "1272.53 - 139.98 - 145.07 + 114.00 = 1101.48 €."
            },
            {
                "id": "Salarios.5",
                "titulo": "Exercício 5 — Carina (Tabela I - 2.º Semestre 2023)",
                "enunciado": "> Salário bruto: 800 €. SS 11% (88,00 €). Retenção IRS (116,00 € - 97,82 € abatimento = 18,18 €). 21 dias a 5,50 €/dia (115,50 €).",
                "pergunta": "Quanto recebeu a Carina no final do mês?",
                "tipo": "float",
                "resposta_correta": 809.32,
                "tolerancia": 0.8,
                "dica": "Faz: 800 - 88.00 - 18.18 + 115.50 = 809.32 €."
            }
        ]
    },

    "Tarefa 5: Salário Bruto à Hora": {
        "resumo_teorico": """
        ### 1. Resumo Teórico
        * **Fórmula Legal do Salário à Hora ($V_h$):**
          $$V_h = \\frac{\\text{Salário Mensal} \\times 12}{52 \\times n}$$
          ($n$ = número de horas semanais contratadas, normalmente $40\\text{ h}$ ou $35\\text{ h}$).
        * **Horas Extraordinárias:** $\\text{Horas Extraordinárias Realizadas} \\times V_h$.
        * As horas extraordinárias acrescem ao salário bruto do mês para cálculo dos impostos.
        """,
        "exemplo_aplicacao": """
        ### 2. Exemplo de Aplicação Resolvido (Maria — Julho de 2023)
        * Salário base: $760\\text{ €}$ por $40\\text{ horas semanais}$.
        * $V_h = \\frac{760 \\times 12}{52 \\times 40} = \\frac{9120}{2080} \\approx 4,38\\text{ €/hora}$.
        * Substituiu uma folga ($8\\text{ horas extra}$): $8 \\times 4,38 = 35,04\\text{ €}$.
        * Total auferido: $760 + 35,04 = 795,04\\text{ €}$.
        """,
        "exercicios": [
            {
                "id": "Hora.1.1",
                "titulo": "Exercício 1.1 — Marco (Mecânico): Salário à Hora",
                "enunciado": "> Salário bruto: 1800 € por 40 horas semanais.",
                "pergunta": "Determina o valor do seu salário à hora (€):",
                "tipo": "float",
                "resposta_correta": 10.38,
                "tolerancia": 0.05,
                "dica": "(1800 * 12) / (52 * 40) = 21600 / 2080 ≈ 10.38 €."
            },
            {
                "id": "Hora.1.2",
                "titulo": "Exercício 1.2 — Marco: Horas Extraordinárias",
                "enunciado": "> Trabalhou 9 horas extraordinárias (5 h no primeiro sábado + 4 h no último). Salário hora: 10,38 €.",
                "pergunta": "Determina o valor a receber em horas extraordinárias no final de julho:",
                "tipo": "float",
                "resposta_correta": 93.42,
                "tolerancia": 0.2,
                "dica": "Multiplica 9 horas por 10.38 € = 93.42 €."
            },
            {
                "id": "Hora.2.1",
                "titulo": "Exercício 2.1 — Carlos (Bar): Salário à Hora",
                "enunciado": "> Salário base de 760 € por 40 horas semanais.",
                "pergunta": "Qual foi o seu vencimento por hora (€)?",
                "tipo": "float",
                "resposta_correta": 4.38,
                "tolerancia": 0.05,
                "dica": "(760 * 12) / (52 * 40) ≈ 4.38 €."
            },
            {
                "id": "Hora.2.2",
                "titulo": "Exercício 2.2 — Carlos: Total no Final de Julho",
                "enunciado": "> 15 horas extra (65,70 €). Bruto total = 825,70 €. SS 11% (90,83 €). IRS retido (30,48 €). Almoça no hotel.",
                "pergunta": "Qual foi o seu vencimento líquido no final do mês de julho?",
                "tipo": "float",
                "resposta_correta": 704.39,
                "tolerancia": 0.8,
                "dica": "Faz: 825.70 - 90.83 - 30.48 = 704.39 €."
            },
            {
                "id": "Hora.3.1",
                "titulo": "Exercício 3.1 — Rosa: Taxa Marginal de Retenção",
                "enunciado": "> Salário de 2789,43 €. Divorciada, 4 dependentes. Tabela II (Não casado, com dependentes).",
                "pergunta": "Indica a taxa marginal máxima de retenção do IRS a que estava sujeita em agosto (%):",
                "tipo": "float",
                "resposta_correta": 38.72,
                "tolerancia": 0.05,
                "dica": "No escalão 'Até 3694,46 €' da Tabela II, a taxa marginal é 38,72%."
            },
            {
                "id": "Hora.3.2",
                "titulo": "Exercício 3.2 — Rosa: Total a Receber em Agosto",
                "enunciado": "> 8 h extra (128,72 €). Bruto total = 2918,15 €. SS 11% (321,00 €). IRS retido (607,76 €). 22 dias a 6 € de refeição (132,00 €).",
                "pergunta": "Qual o valor líquido total a receber no final de agosto?",
                "tipo": "float",
                "resposta_correta": 2121.39,
                "tolerancia": 1.5,
                "dica": "2918.15 - 321.00 - 607.76 + 132.00 = 2121.39 €."
            },
            {
                "id": "Hora.4.1",
                "titulo": "Exercício 4 — Maria do Restaurante",
                "enunciado": "> Salário de 902 € (40 h/sem). Recebeu 58 € por 12 horas extraordinárias e afirma que houve engano.",
                "pergunta": "Concordas com a Maria?",
                "tipo": "choice",
                "opcoes": [
                    "Selecione...",
                    "Sim, concordo. O valor da hora é cerca de 5,20 €, logo por 12 horas devia receber 62,45 € e não 58 €",
                    "Não concordo, os 58 € correspondem exatamente ao valor devido",
                    "Não concordo, a Maria devia ter recebido menos do que 58 €"
                ],
                "resposta_correta": "Sim, concordo. O valor da hora é cerca de 5,20 €, logo por 12 horas devia receber 62,45 € e não 58 €",
                "dica": "Hora = (902 * 12) / 2080 ≈ 5.2038 €. Por 12 horas devia auferir 62.45 €."
            },
            {
                "id": "Hora.5.1",
                "titulo": "Exercício 5 — Amiga da Maria no Hotel",
                "enunciado": "> Amiga recebe 1000 € por 35 h semanais (6,59 €/h). Fez 8 horas extraordinárias no mês.",
                "pergunta": "Quem recebeu mais em horas extraordinárias: a Maria (58 €) ou a sua amiga?",
                "tipo": "choice",
                "opcoes": [
                    "Selecione...",
                    "A Maria, pois recebeu 58 € enquanto a sua amiga recebeu cerca de 52,75 € (8 h x 6,59 €/h)",
                    "A amiga da Maria, porque tem um salário mensal mais alto",
                    "Receberam ambas exatamente a mesma quantia"
                ],
                "resposta_correta": "A Maria, pois recebeu 58 € enquanto a sua amiga recebeu cerca de 52,75 € (8 h x 6,59 €/h)",
                "dica": "A amiga ganha 8 * 6.59 = 52.75 €, valor inferior aos 58 € recebidos pela Maria."
            }
        ]
    },

    "Tarefa 6: Cálculo do IRS Anual": {
        "resumo_teorico": """
        ### 1. Resumo Teórico
        * **1. Rendimento Bruto Anual:** $\\sum (\\text{Salário Mensal} \\times 14)$.
        * **2. Rendimento Coletável:**
          $$\\text{Coletável} = \\frac{\\text{Bruto Anual} - \\text{Deduções Específicas (4104 € por titular)}}{\\text{Quociente Familiar (2 para casal)}}$$
        * **3. Coleta Total:** $[(\\text{Coletável} \\times \\text{Taxa}) - \\text{Parcela a Abater}] \\times \\text{Quociente Familiar}$.
        * **4. Saldo Final:** $\\text{Coleta Líquida} - \\text{Retenções na Fonte já efetuadas}$.
        """,
        "exemplo_aplicacao": """
        ### 2. Exemplo de Aplicação Resolvido (Mariana e Afonso — Lisboa 2023)
        * Rendimentos: Mariana ($1200 \\times 14 = 16\\,800\\text{ €}$) | Afonso ($1340 \\times 14 = 18\\,760\\text{ €}$). Bruto = $35\\,560\\text{ €}$.
        * Sem deduções: Coletável = $35\\,560 / 2 = 17\\,780\\text{ €}$ (4.º escalão: taxa $28,5\%$, abater $1426,65\\text{ €}$).
        * Coleta total = $[(17\\,780 \\times 0,285) - 1426,65] \\times 2 = 3640,65 \\times 2 = 7281,30\\text{ €}$.
        * O casal vai **pagar 7281,30 € de IRS**.
        """,
        "exercicios": [
            {
                "id": "IRS.1.1",
                "titulo": "Exercício 1.1 — Joana e Miguel (Porto 2023)",
                "enunciado": "> Joana (1200 € x 14 = 16 800 €) e Miguel (1890 € x 14 = 26 460 €). Bruto = 43 260 €. Coletável (/2) = 21 630 € (5.º escalão: 35%, abater 2772,14 €).",
                "pergunta": "Quanto pagaram de IRS no total? (Arredonda às centésimas):",
                "tipo": "float",
                "resposta_correta": 9596.72,
                "tolerancia": 1.0,
                "dica": "[(21 630 * 0.35) - 2772.14] * 2 = 4798.36 * 2 = 9596.72 €."
            },
            {
                "id": "IRS.1.2",
                "titulo": "Exercício 1.2 — Mariana e Afonso com Deduções Específicas",
                "enunciado": "> Se Mariana e Afonso considerarem as deduções de 4104 € cada (8208 €), coletável passa para 13 676 € (3.º escalão: 26,5%, abater 1106,73 €).",
                "pergunta": "O valor que vão pagar de IRS é distinto?",
                "tipo": "choice",
                "opcoes": [
                    "Selecione...",
                    "Sim, é distinto: com as deduções específicas pagam 5034,82 € (uma poupança de 2246,48 € face aos 7281,30 €)",
                    "Não, o valor a pagar mantém-se exatamente o mesmo de 7281,30 €",
                    "Sim, passam a pagar mais imposto"
                ],
                "resposta_correta": "Sim, é distinto: com as deduções específicas pagam 5034,82 € (uma poupança de 2246,48 € face aos 7281,30 €)",
                "dica": "[(13 676 * 0.265) - 1106.73] * 2 = 5034.82 €. Poupança direta de 2246.48 €."
            },
            {
                "id": "IRS.2.1",
                "titulo": "Exercício 2.1 — Rita e Afonso: Rendimento Bruto Anual",
                "enunciado": "> Rita (1050 € mensais) e Afonso (1010 € mensais), recebem 14 meses ao ano.",
                "pergunta": "Determina o rendimento bruto anual do casal (€):",
                "tipo": "int",
                "resposta_correta": 28840,
                "tolerancia": 0,
                "dica": "(1050 * 14) + (1010 * 14) = 14700 + 14140 = 28840 €."
            },
            {
                "id": "IRS.2.2",
                "titulo": "Exercício 2.2 — Rita e Afonso: Rendimento Coletável",
                "enunciado": "> Declaração conjunta sem deduções (quociente familiar = 2).",
                "pergunta": "Apura o rendimento coletável (€):",
                "tipo": "int",
                "resposta_correta": 14420,
                "tolerancia": 0,
                "dica": "Divide 28840 por 2 = 14420 €."
            },
            {
                "id": "IRS.2.3",
                "titulo": "Exercício 2.3 — Rita e Afonso: Coleta Total a Pagar",
                "enunciado": "> 3.º escalão (]11 284; 15 992]): taxa = 26,5%, parcela a abater = 1106,73 €.",
                "pergunta": "Calcula o valor da coleta total (IRS a pagar):",
                "tipo": "float",
                "resposta_correta": 5429.14,
                "tolerancia": 1.0,
                "dica": "[(14 420 * 0.265) - 1106.73] * 2 = 2714.57 * 2 = 5429.14 €."
            },
            {
                "id": "IRS.3.1",
                "titulo": "Exercício 3 — Manuel (Solteiro em Faro)",
                "enunciado": "> 1300 € mensais (14 meses = 18 200 €). Solteiro (coletável = 18 200 €). 4.º escalão: taxa 28,5%, abater 1426,65 €.",
                "pergunta": "Determina o valor que o Manuel pagou de IRS (€):",
                "tipo": "float",
                "resposta_correta": 3760.35,
                "tolerancia": 1.0,
                "dica": "(18 200 * 0.285) - 1426.65 = 5187.00 - 1426.65 = 3760.35 €."
            },
            {
                "id": "IRS.4.1",
                "titulo": "Exercício 4.1 — Eugénia e Augusto (Açores 2022): Coletável",
                "enunciado": "> Eugénia (2530 € x 14 = 35 420 €) e Augusto (2300 € x 14 = 32 200 €). Bruto = 67 620 €.",
                "pergunta": "Apura o rendimento coletável sem deduções (€):",
                "tipo": "int",
                "resposta_correta": 33810,
                "tolerancia": 0,
                "dica": "67620 / 2 = 33810 €."
            },
            {
                "id": "IRS.4.2",
                "titulo": "Exercício 4.2 — Eugénia e Augusto: IRS a Pagar",
                "enunciado": "> 6.º escalão Açores (taxa 25,9%, abater 2146,76 €).",
                "pergunta": "Determina o valor do IRS a pagar (€):",
                "tipo": "float",
                "resposta_correta": 13220.06,
                "tolerancia": 1.5,
                "dica": "[(33 810 * 0.259) - 2146.76] * 2 = 6610.03 * 2 = 13220.06 €."
            },
            {
                "id": "IRS.4.3",
                "titulo": "Exercício 4.3 — Impacto das Deduções Específicas",
                "enunciado": "> Deduções específicas de 4104 € cada (8208 €). Mantêm-se no mesmo escalão dos Açores com taxa de 25,9%.",
                "pergunta": "Qual teria sido a diferença (poupança) no valor do IRS face à alínea anterior (€)?",
                "tipo": "float",
                "resposta_correta": 2125.87,
                "tolerancia": 1.0,
                "dica": "Poupança direta = 8208 * 0.259 = 2125.87 € (pagam 11 094.19 € em vez de 13 220.06 €)."
            }
        ]
    }
}

# ----------------------------------------------------
# 4. GESTÃO DE ESTADO DA SESSÃO
# ----------------------------------------------------
if "tarefa_selecionada" not in st.session_state:
    st.session_state.tarefa_selecionada = list(DADOS_TAREFAS.keys())[0]
if "indice_pergunta" not in st.session_state:
    st.session_state.indice_pergunta = 0
if "tentativas" not in st.session_state:
    st.session_state.tentativas = 0
if "tempo_inicio_questao" not in st.session_state:
    st.session_state.tempo_inicio_questao = time.time()
if "data_inicio_tarefa" not in st.session_state:
    st.session_state.data_inicio_tarefa = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
if "data_reinicio_sessao" not in st.session_state:
    st.session_state.data_reinicio_sessao = ""
if "respostas_certas_historico" not in st.session_state:
    st.session_state.respostas_certas_historico = {} # {id_ex: {"resposta": ..., "tempo": ..., "tentativas": ...}}

# ----------------------------------------------------
# 5. BARRA LATERAL (SELEÇÃO, IDENTIFICAÇÃO E AUDITORIA)
# ----------------------------------------------------
with st.sidebar:
    if os.path.exists(LOGO_PATH):
        try:
            st.image(LOGO_PATH, width="stretch")
        except TypeError:
            st.image(LOGO_PATH)
    else:
        st.title("EPDR Grândola")

    st.subheader("📋 Seleção da Tarefa")
    tarefa_escolhida = st.selectbox(
        "Escolhe a Tarefa:",
        list(DADOS_TAREFAS.keys()),
        index=list(DADOS_TAREFAS.keys()).index(st.session_state.tarefa_selecionada)
    )

    if tarefa_escolhida != st.session_state.tarefa_selecionada:
        st.session_state.tarefa_selecionada = tarefa_escolhida
        st.session_state.indice_pergunta = 0
        st.session_state.tentativas = 0
        st.session_state.data_inicio_tarefa = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.data_reinicio_sessao = ""
        st.session_state.tempo_inicio_questao = time.time()
        st.session_state.respostas_certas_historico = {}
        st.rerun()

    st.markdown("---")
    st.subheader("👤 Identificação do Aluno")
    nome_aluno = st.text_input("Nome Completo:", key="input_nome").strip()
    turma_aluno = st.selectbox(
        "Turma:",
        ["10º TCP/TRB", "10º TPA/TOE"],
        key="select_turma"
    )

    st.caption(f"⏱️ **Início da Tarefa:** {st.session_state.data_inicio_tarefa}")
    if st.session_state.data_reinicio_sessao:
        st.caption(f"🔄 **Reinício de Sessão:** {st.session_state.data_reinicio_sessao}")

    # RETOMAR PROGRESSO
    if st.button("🔄 Retomar Meu Progresso", use_container_width=True):
        if not nome_aluno:
            st.warning("Insere o teu nome para recuperares o progresso!")
        elif os.path.exists(CSV_PATH):
            try:
                df_rec = pd.read_csv(CSV_PATH, on_bad_lines='skip')
                df_aluno = df_rec[
                    (df_rec["Aluno"].str.strip().str.lower() == nome_aluno.lower()) &
                    (df_rec["Tarefa"] == st.session_state.tarefa_selecionada) &
                    (df_rec["Resultado"] == "Correta")
                ]
                
                lista_exercicios = DADOS_TAREFAS[st.session_state.tarefa_selecionada]["exercicios"]
                if not df_aluno.empty:
                    certos_dict = {}
                    for _, row in df_aluno.iterrows():
                        certos_dict[str(row["Exercicio"])] = {
                            "resposta": row["Resposta_Dada"],
                            "tempo": row["Tempo_Segundos"],
                            "tentativas": row["Tentativas"]
                        }
                    
                    prox_idx = 0
                    for i, ex in enumerate(lista_exercicios):
                        if str(ex["id"]) in certos_dict:
                            prox_idx = i + 1
                        else:
                            break
                    
                    st.session_state.respostas_certas_historico = certos_dict
                    st.session_state.indice_pergunta = min(prox_idx, len(lista_exercicios))
                    st.session_state.tentativas = 0
                    st.session_state.data_inicio_tarefa = df_aluno["Data_Inicio_Tarefa"].iloc[0]
                    st.session_state.data_reinicio_sessao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.tempo_inicio_questao = time.time()
                    
                    guardar_registo(
                        nome=nome_aluno,
                        turma=turma_aluno,
                        tarefa=st.session_state.tarefa_selecionada,
                        data_inicio=st.session_state.data_inicio_tarefa,
                        data_reinicio=st.session_state.data_reinicio_sessao,
                        ex_id=f"Retoma-{prox_idx}",
                        pergunta="Sessão retomada",
                        resposta="Reinício",
                        correta=True,
                        tentativas=0,
                        tempo_segundos=0,
                        tipo_evento="Reinicio"
                    )
                    st.success(f"Progresso recuperado! Estás no exercício {min(prox_idx + 1, len(lista_exercicios))}.")
                    st.rerun()
                else:
                    st.info("Não existem exercícios previamente concluídos nesta tarefa.")
            except Exception:
                st.error("Erro ao ler os registos.")
        else:
            st.info("Ainda não existem registos guardados.")

    # TERMINAR SESSÃO
    if st.button("🚪 Terminar e Sair por hoje", use_container_width=True):
        if nome_aluno:
            agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            guardar_registo(
                nome=nome_aluno,
                turma=turma_aluno,
                tarefa=st.session_state.tarefa_selecionada,
                data_inicio=st.session_state.data_inicio_tarefa,
                data_reinicio=st.session_state.data_reinicio_sessao,
                ex_id="Saida",
                pergunta="Aluno assinalou fecho de sessão",
                resposta="Fecho",
                correta=True,
                tentativas=0,
                tempo_segundos=0,
                tipo_evento="Fecho"
            )
            st.success(f"Sessão terminada às {agora}. Podes fechar o browser com segurança!")
        else:
            st.warning("Insere o teu nome antes de sair.")

    st.markdown("---")
    st.subheader("🔒 Acesso do Professor")
    senha_docente = st.text_input("Palavra-passe docente:", type="password")

    if senha_docente == "epdrg2026":
        st.success("Sessão docente autenticada.")
        if os.path.exists(CSV_PATH):
            try:
                df_geral = pd.read_csv(CSV_PATH, on_bad_lines='skip')
            except Exception:
                df_geral = pd.DataFrame()
            
            if not df_geral.empty and "Aluno" in df_geral.columns:
                st.metric("Total de Registos", len(df_geral))
                st.metric("Alunos Registados", df_geral["Aluno"].nunique())
                
                st.download_button(
                    label="📥 Descarregar CSV Completo",
                    data=df_geral.to_csv(index=False, encoding="utf-8-sig"),
                    file_name="respostas_alunos_epdrg.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # MATRIZ EM DIRETO SEM PRECISAR DE EXPANDER
                st.markdown("#### 📍 Estado dos Alunos")
                df_estado = (
                    df_geral.sort_values(by="Data_Hora")
                    .groupby(["Aluno", "Turma", "Tarefa"], as_index=False)
                    .last()
                )
                cols_estado = [
                    c for c in [
                        "Aluno", "Turma", "Tarefa", "Data_Inicio_Tarefa", 
                        "Data_Reinicio_Sessao", "Exercicio", "Resposta_Dada", "Resultado", "Data_Hora"
                    ] if c in df_estado.columns
                ]
                df_exibir = df_estado[cols_estado].rename(columns={
                    "Data_Inicio_Tarefa": "Início",
                    "Data_Reinicio_Sessao": "Reinício",
                    "Data_Hora": "Última Atividade",
                    "Exercicio": "Exercício",
                    "Resposta_Dada": "Última Resposta"
                })
                try:
                    st.dataframe(df_exibir, width="stretch")
                except TypeError:
                    st.dataframe(df_exibir)
            else:
                st.info("Ainda não existem registos gravados.")

# ----------------------------------------------------
# 6. CORPO PRINCIPAL: TEORIA, EXEMPLOS E EXERCÍCIOS
# ----------------------------------------------------
tarefa_dados = DADOS_TAREFAS[st.session_state.tarefa_selecionada]
lista_exercicios = tarefa_dados["exercicios"]
total_exercicios = len(lista_exercicios)

st.title(f"🎓 {st.session_state.tarefa_selecionada}")
st.caption("Módulo P1: Modelos Matemáticos para a Cidadania | EPDR Grândola")

# SEPARADORES OBRIGATÓRIOS: RESUMO TEÓRICO E EXEMPLO RESOLVIDO
tab_teoria, tab_exemplo = st.tabs(["📖 1. Resumo Teórico", "💡 2. Exemplo de Aplicação Resolvido"])
with tab_teoria:
    st.markdown(tarefa_dados["resumo_teorico"])
with tab_exemplo:
    st.markdown(tarefa_dados["exemplo_aplicacao"])

st.markdown("---")
st.subheader("✍️ 3. Caderno de Exercícios")

progresso = min(st.session_state.indice_pergunta / total_exercicios, 1.0)
st.progress(progresso, text=f"Progresso: {min(st.session_state.indice_pergunta, total_exercicios)} de {total_exercicios} exercícios concluídos")

# ----------------------------------------------------
# 7. EXIBIÇÃO PERMANENTE DOS EXERCÍCIOS CONCLUÍDOS
# ----------------------------------------------------
for i in range(min(st.session_state.indice_pergunta, total_exercicios)):
    ex_resolvido = lista_exercicios[i]
    info_resolucao = st.session_state.respostas_certas_historico.get(str(ex_resolvido["id"]), {})
    resp_feita = info_resolucao.get("resposta", ex_resolvido["resposta_correta"])
    tent_feita = info_resolucao.get("tentativas", "-")
    tempo_feito = info_resolucao.get("tempo", "-")
    
    with st.container(border=True):
        st.markdown(f"#### ✅ {ex_resolvido['titulo']}")
        st.markdown(ex_resolvido["enunciado"])
        st.markdown(f"**Pergunta:** {ex_resolvido['pergunta']}")
        st.success(
            f"🎯 **Resolvido com Sucesso!** | A tua resposta: `{resp_feita}` | "
            f"Tentativas: `{tent_feita}` | Tempo: `{tempo_feito}s`"
        )

# ----------------------------------------------------
# 8. EXERCÍCIO ATIVO OU MENSAGEM DE CONCLUSÃO
# ----------------------------------------------------
if st.session_state.indice_pergunta >= total_exercicios:
    st.balloons()
    st.success(f"🏆 **Parabéns, {nome_aluno if nome_aluno else 'aluno'}! Concluíste na íntegra a {st.session_state.tarefa_selecionada}!**")
    st.info("Podes rever todas as tuas respostas acima. O teu professor tem o registo completo de horas e desempenho arquivado.")
else:
    q_atual = lista_exercicios[st.session_state.indice_pergunta]
    
    with st.container(border=True):
        st.markdown(f"### 📍 Exercício em Resolução: {q_atual['titulo']}")
        st.markdown(q_atual["enunciado"])
        st.markdown(f"**👉 Pergunta:** {q_atual['pergunta']}")

        if not nome_aluno:
            st.warning("⚠️ Por favor, insere o teu nome completo na barra lateral para poderes responder.")
        else:
            with st.form(key=f"form_ativo_{st.session_state.tarefa_selecionada}_{q_atual['id']}"):
                resposta_dada = None

                if q_atual["tipo"] == "int":
                    resposta_dada = st.number_input("A tua resposta (número inteiro):", step=1, value=0)
                elif q_atual["tipo"] == "float":
                    resposta_dada = st.number_input("A tua resposta (valor numérico):", step=0.1, format="%.2f", value=0.0)
                elif q_atual["tipo"] == "choice":
                    resposta_dada = st.selectbox("Escolhe a opção correta:", q_atual["opcoes"])

                btn_submeter = st.form_submit_button("Submeter Resposta 🚀", use_container_width=True)

                if btn_submeter:
                    st.session_state.tentativas += 1
                    tempo_gasto = time.time() - st.session_state.tempo_inicio_questao

                    acertou = False
                    if q_atual["tipo"] == "int":
                        acertou = (int(resposta_dada) == int(q_atual["resposta_correta"]))
                    elif q_atual["tipo"] == "float":
                        acertou = abs(float(resposta_dada) - float(q_atual["resposta_correta"])) <= q_atual["tolerancia"]
                    elif q_atual["tipo"] == "choice":
                        acertou = (resposta_dada == q_atual["resposta_correta"])

                    # Registo na telemetria
                    guardar_registo(
                        nome=nome_aluno,
                        turma=turma_aluno,
                        tarefa=st.session_state.tarefa_selecionada,
                        data_inicio=st.session_state.data_inicio_tarefa,
                        data_reinicio=st.session_state.data_reinicio_sessao,
                        ex_id=q_atual["id"],
                        pergunta=q_atual["titulo"],
                        resposta=resposta_dada,
                        correta=acertou,
                        tentativas=st.session_state.tentativas,
                        tempo_segundos=tempo_gasto,
                        tipo_evento="Conclusão" if (acertou and st.session_state.indice_pergunta + 1 == total_exercicios) else "Resposta"
                    )

                    if acertou:
                        st.session_state.respostas_certas_historico[str(q_atual["id"])] = {
                            "resposta": str(resposta_dada),
                            "tempo": round(tempo_gasto, 1),
                            "tentativas": st.session_state.tentativas
                        }
                        st.session_state.indice_pergunta += 1
                        st.session_state.tentativas = 0
                        st.session_state.tempo_inicio_questao = time.time()
                        st.rerun()
                    else:
                        st.error(f"❌ A resposta `{resposta_dada}` não está correta.")
                        st.info(f"💡 **Dica do Tutor:** {q_atual['dica']}")
