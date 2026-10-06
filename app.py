import streamlit as st
import pandas as pd
from datetime import datetime
import time
import os

# ----------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA E CAMINHOS
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
# 3. BASE DE DADOS COMPLETA DAS 4 TAREFAS
# ----------------------------------------------------
DADOS_TAREFAS = {
    "Tarefa 1: Maioria Simples e Maioria Absoluta": {
        "resumo_teorico": """
        #### Apoio Teórico — Sistemas Eleitorais
        * **Votos Válidos:** $\\text{Votantes} - (\\text{Votos Brancos} + \\text{Votos Nulos})$
        * **Taxa de Abstenção:** $\\frac{\\text{Inscritos} - \\text{Votantes}}{\\text{Inscritos}} \\times 100$
        * **Maioria Simples (Relativa):** Vence o candidato/opção com o maior número de votos válidos.
        * **Maioria Absoluta:** Exige mais de 50% dos votos válidos (metade mais 1 nos votos inteiros). Se ninguém atingir, há 2.ª volta com os dois mais votados.
        """,
        "exercicios": [
            {
                "id": "1.1.1",
                "titulo": "Exercício 1.1.1 — Votos Validamente Expressos (1976)",
                "enunciado_geral": "> **1.ª eleição presidencial da democracia (1976)**\n> * Votantes: 4 881 125 | Brancos: 20 253 | Nulos: 43 242",
                "pergunta": "Determine o número total de votos validamente expressos:",
                "tipo": "int",
                "resposta_correta": 4817630,
                "tolerancia": 0,
                "dica": "Votos Válidos = Votantes - Brancos - Nulos (4 881 125 - 20 253 - 43 242)."
            },
            {
                "id": "1.1.2",
                "titulo": "Exercício 1.1.2 — Taxa de Abstenção",
                "enunciado_geral": "> Inscritos: 6 467 480 | Votantes: 4 881 125",
                "pergunta": "Calcula a percentagem de abstenção (arredondada às décimas, ex: 24.5):",
                "tipo": "float",
                "resposta_correta": 24.5,
                "tolerancia": 0.15,
                "dica": "Abstenção = (6 467 480 - 4 881 125) / 6 467 480 * 100."
            },
            {
                "id": "1.1.3",
                "titulo": "Exercício 1.1.3 — Percentagem do Candidato Mais Votado",
                "enunciado_geral": "> António Ramalho Eanes obteve 2 967 137 votos num total de 4 817 630 votos válidos.",
                "pergunta": "Calcula a percentagem de votos obtida por este candidato (arredondada às décimas):",
                "tipo": "float",
                "resposta_correta": 61.6,
                "tolerancia": 0.2,
                "dica": "Divide 2 967 137 por 4 817 630 e multiplica por 100."
            },
            {
                "id": "1.2",
                "titulo": "Exercício 1.2 — Presidente Eleito",
                "enunciado_geral": "> Para ser eleito na 1.ª volta é necessário obter mais de 50% dos votos válidos.",
                "pergunta": "Quem foi o candidato eleito Presidente da República em 1976?",
                "tipo": "choice",
                "opcoes": ["Selecione...", "António Ramalho Eanes", "José Pinheiro de Azevedo", "Otelo Saraiva de Carvalho"],
                "resposta_correta": "António Ramalho Eanes",
                "dica": "António Ramalho Eanes obteve mais de 61% dos votos válidos."
            },
            {
                "id": "2.1",
                "titulo": "Exercício 2.1 — Percentagem de Votos Válidos na Turma",
                "enunciado_geral": "> Numa turma de 23 alunos faltou 1 aluna (22 votantes). Houve 21 votos válidos e 1 branco.",
                "pergunta": "Calcula a percentagem de votos válidos face aos votantes (arredonda às centésimas, ex: 95.45):",
                "tipo": "float",
                "resposta_correta": 95.45,
                "tolerancia": 0.05,
                "dica": "(21 / 22) * 100."
            },
            {
                "id": "2.3",
                "titulo": "Exercício 2.3 — Mínimo para Maioria Absoluta",
                "enunciado_geral": "> Votos válidos apurados: 21 votos.",
                "pergunta": "Qual o número mínimo de votos inteiros para vencer por maioria absoluta?",
                "tipo": "int",
                "resposta_correta": 11,
                "tolerancia": 0,
                "dica": "Metade de 21 é 10,5. O menor número inteiro superior é 11."
            }
        ]
    },

    "Tarefa 2: Método da Borda": {
        "resumo_teorico": """
        #### Apoio Teórico — Método da Borda
        * Numa eleição com $N$ opções:
          * 1.ª preferência: $N$ pontos;
          * 2.ª preferência: $N - 1$ pontos;
          * ... última preferência: 1 ponto.
        * Multiplica-se o total de votos de cada coluna pelos respetivos pontos e soma-se por opção.
        * Vence quem acumular o **maior total de pontos**.
        """,
        "exercicios": [
            {
                "id": "Borda.1.1",
                "titulo": "Exercício 1.1 — Representante no Projeto de Mandarim",
                "enunciado_geral": (
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
                "dica": "Pontuações: B = 140, R = 131, C = 105, M = 94. O Bernardo vence."
            },
            {
                "id": "Borda.1.2",
                "titulo": "Exercício 1.2 — Comparação com Maioria Simples",
                "enunciado_geral": "> Primeiras escolhas: Bernardo (14 votos), Ricardo (21 votos), Manuel (9 votos), Célia (3 votos).",
                "pergunta": "Por maioria simples, o aluno eleito seria o mesmo que pelo método de Borda?",
                "tipo": "choice",
                "opcoes": [
                    "Selecione...",
                    "Não, por maioria simples seria o Ricardo (21 votos)",
                    "Sim, continuaria a ser o Bernardo"
                ],
                "resposta_correta": "Não, por maioria simples seria o Ricardo (21 votos)",
                "dica": "Na 1.ª preferência o Ricardo foi o mais votado com 21 votos."
            },
            {
                "id": "Borda.2.1",
                "titulo": "Exercício 2.1 — Votação no Restaurante",
                "enunciado_geral": "> Pratos: Carne de porco (C), Polvo (P), Bacalhau (B). Colunas: 12 votos, 5 votos e 9 votos.",
                "pergunta": "Quantos clientes estavam no restaurante (total de boletins)?",
                "tipo": "int",
                "resposta_correta": 26,
                "tolerancia": 0,
                "dica": "12 + 5 + 9 = 26 clientes."
            },
            {
                "id": "Borda.2.2",
                "titulo": "Exercício 2.2 — Prato Escolhido pelo Método de Borda",
                "enunciado_geral": "> Pontos por preferência: 1.ª = 3 pts, 2.ª = 2 pts, 3.ª = 1 pt.",
                "pergunta": "Qual foi o prato vencedor pelo método de Borda?",
                "tipo": "choice",
                "opcoes": ["Selecione...", "Bacalhau à Gomes de Sá (B)", "Carne de porco com amêijoas (C)", "Polvo à Lagareiro (P)"],
                "resposta_correta": "Bacalhau à Gomes de Sá (B)",
                "dica": "Pontos: Bacalhau = 56, Carne de porco = 55, Polvo = 45."
            },
            {
                "id": "Borda.3",
                "titulo": "Exercício 3 — Escolha do Cartaz",
                "enunciado_geral": "> Cartazes A, B e C com 28 alunos. Distribuição: Coluna 1 (12), Coluna 2 (6), Coluna 3 (10).",
                "pergunta": "Qual foi o cartaz escolhido pelo método de Borda?",
                "tipo": "choice",
                "opcoes": ["Selecione...", "Cartaz A", "Cartaz B", "Cartaz C"],
                "resposta_correta": "Cartaz C",
                "dica": "Cartaz C obteve 62 pontos contra 58 do Cartaz A e 48 do Cartaz B."
            }
        ]
    },

    "Tarefa 3: Método de Hondt e Sainte-Laguë": {
        "resumo_teorico": """
        #### Apoio Teórico — Métodos Proporcionais
        * **Método de Hondt:** Divisões sucessivas por **1, 2, 3, 4, 5...** (favorece alternativas com mais votos).
        * **Método de Sainte-Laguë:** Divisões sucessivas apenas por números ímpares: **1, 3, 5, 7...** (favorece listas menores).
        """,
        "exercicios": [
            {
                "id": "Hondt.1.1",
                "titulo": "Exercício 1.1 — Prémios nas Modalidades Desportivas",
                "enunciado_geral": "> Voleibol (211), Futebol (145), Basquetebol (103), Dança (78). 5 prémios por Hondt.",
                "pergunta": "Existe alguma modalidade que não recebeu nenhum prémio?",
                "tipo": "choice",
                "opcoes": ["Selecione...", "Sim, a Dança ficou com 0 prémios", "Não, todas receberam pelo menos 1 prémio"],
                "resposta_correta": "Sim, a Dança ficou com 0 prémios",
                "dica": "Prémios: Voleibol (2), Futebol (2), Basquetebol (1), Dança (0)."
            },
            {
                "id": "Hondt.2",
                "titulo": "Exercício 2 — Bicicletas no Pré-Escolar",
                "enunciado_geral": "> Alunos por sala: Vermelha (26), Azul (22), Amarela (18), Verde (15). Distribuem-se 6 bicicletas por Hondt.",
                "pergunta": "Quantas bicicletas foram atribuídas à sala Vermelha?",
                "tipo": "int",
                "resposta_correta": 2,
                "tolerancia": 0,
                "dica": "A sala Vermelha obteve o 1.º quociente (26) e o 5.º quociente (13)."
            },
            {
                "id": "Hondt.5",
                "titulo": "Exercício 5 — Contentores de Óleos na Vila Piscatória",
                "enunciado_geral": "> Votos: Conserva (4235), Restaurantes (1240), Zona Ind. (856), Mercado (745). 6 contentores por Hondt.",
                "pergunta": "Quantos contentores foram colocados perto do Mercado do Peixe?",
                "tipo": "int",
                "resposta_correta": 0,
                "tolerancia": 0,
                "dica": "Os 6 contentores foram para a Conserva (4), Restaurantes (1) e Zona Industrial (1)."
            },
            {
                "id": "SaintLague.6",
                "titulo": "Exercício 6 — Sainte-Laguë vs Hondt (Bicicletas)",
                "enunciado_geral": "> No caso das 6 bicicletas (salas com 18, 22, 26 e 15 alunos), aplicando Sainte-Laguë (/1 e /3).",
                "pergunta": "Um aluno afirmou que por Sainte-Laguë a distribuição seria diferente da de Hondt. Tem razão?",
                "tipo": "choice",
                "opcoes": [
                    "Selecione...",
                    "Não tem razão, a distribuição mantém-se idêntica (Vermelha: 2, Azul: 2, Amarela: 1, Verde: 1)",
                    "Sim, a sala Verde ganharia mais uma bicicleta"
                ],
                "resposta_correta": "Não tem razão, a distribuição mantém-se idêntica (Vermelha: 2, Azul: 2, Amarela: 1, Verde: 1)",
                "dica": "Os 6 maiores quocientes por Sainte-Laguë continuam a dar a mesma distribuição."
            }
        ]
    },

    "Tarefa 4: Matemática nos Salários": {
        "resumo_teorico": """
        #### Apoio Teórico — Salário Líquido e Retenções
        * **Segurança Social (SS):** 11% da Remuneração Base.
        * **Retenção de IRS:** $\\text{Remuneração Base} \\times \\text{Taxa IRS}$
        * **Salário Líquido:** $\\text{Remuneração Base} - \\text{SS} - \\text{IRS}$
        * **Subsídio de Refeição:** $\\text{Dias Trabalhados} \\times \\text{Valor Diário}$
        * **Líquido a Receber:** $\\text{Salário Líquido} + \\text{Subsídio de Refeição}$
        """,
        "exercicios": [
            {
                "id": "Salarios.1",
                "titulo": "Exercício 1 — Vencimento Líquido do Mateus",
                "enunciado_geral": "> Salário base: 1956,40 €. Desconto SS: 11%. Retenção IRS: 14,6%. Trabalhou 22 dias a 5,80 €/dia de refeição.",
                "pergunta": "Qual foi o valor líquido total que o Mateus recebeu no final do mês? (Arredonda às centésimas):",
                "tipo": "float",
                "resposta_correta": 1583.17,
                "tolerancia": 0.5,
                "dica": "Líquido base = 1956.40 - 215.20 (SS) - 285.63 (IRS) = 1455.57 €. Mais subsídio (22 * 5.80 = 127.60 €) = 1583.17 €."
            },
            {
                "id": "Salarios.2",
                "titulo": "Exercício 2 — Vencimento do Carlos (Fev 2023)",
                "enunciado_geral": "> Salário bruto: 975,00 €. SS: 11% (107,25 €). IRS: 5% (48,75 €). Subsídio: 20 dias a 5,90 €/dia.",
                "pergunta": "Qual foi o valor líquido total recebido pelo Carlos em fevereiro de 2023?",
                "tipo": "float",
                "resposta_correta": 937.00,
                "tolerancia": 0.5,
                "dica": "Líquido base = 975 - 107.25 - 48.75 = 819.00 €. Mais 118.00 € de subsídio = 937.00 €."
            },
            {
                "id": "Salarios.3",
                "titulo": "Exercício 3 — Retenção de IRS da Mariana",
                "enunciado_geral": "> Salário bruto: 1700 €. Escalão com taxa de retenção de 16,1% para 2 dependentes.",
                "pergunta": "Qual é o valor em euros descontado para o IRS mensalmente?",
                "tipo": "float",
                "resposta_correta": 273.70,
                "tolerancia": 0.2,
                "dica": "1700 * 0.161 = 273.70 €."
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
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "assistant", "content": "👋 Olá! Sou o teu Tutor de Matemática para a Cidadania. Escolhe a tarefa na barra lateral e começa a resolver!"}
    ]

# ----------------------------------------------------
# 5. BARRA LATERAL (SELEÇÃO, IDENTIFICAÇÃO E PROFESSOR)
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
        st.session_state.mensagens = [
            {"role": "assistant", "content": f"Mudaste para a **{tarefa_escolhida}**. Lê o resumo de apoio e bom trabalho!"}
        ]
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

    # BOTÃO PARA RECUPERAR E REGISTAR REINÍCIO
    if st.button("🔄 Retomar Meu Progresso", use_container_width=True):
        if not nome_aluno:
            st.warning("Insere o teu nome para recuperares o teu progresso!")
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
                    exercicios_concluidos = set(df_aluno["Exercicio"].astype(str).tolist())
                    prox_idx = 0
                    for i, ex in enumerate(lista_exercicios):
                        if str(ex["id"]) in exercicios_concluidos:
                            prox_idx = i + 1
                        else:
                            break
                    st.session_state.indice_pergunta = min(prox_idx, len(lista_exercicios))
                    st.session_state.tentativas = 0
                    st.session_state.data_inicio_tarefa = df_aluno["Data_Inicio_Tarefa"].iloc[0]
                    # Carimbo de hora de reinício
                    st.session_state.data_reinicio_sessao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.tempo_inicio_questao = time.time()
                    
                    # Guarda registo do reinício no CSV
                    guardar_registo(
                        nome=nome_aluno,
                        turma=turma_aluno,
                        tarefa=st.session_state.tarefa_selecionada,
                        data_inicio=st.session_state.data_inicio_tarefa,
                        data_reinicio=st.session_state.data_reinicio_sessao,
                        ex_id=f"Retoma-{prox_idx}",
                        pergunta="Sessão retomada pelo aluno",
                        resposta="Reinício",
                        correta=True,
                        tentativas=0,
                        tempo_segundos=0,
                        tipo_evento="Reinicio"
                    )

                    st.session_state.mensagens = [
                        {"role": "assistant", "content": f"🎉 Bem-vindo de volta, **{nome_aluno}**! Recuperámos o teu trabalho. Estás no exercício {min(prox_idx + 1, len(lista_exercicios))}."}
                    ]
                    st.rerun()
                else:
                    st.info("Não foram encontradas respostas corretas registadas com esse nome nesta tarefa.")
            except Exception:
                st.error("Erro ao ler o histórico de dados.")
        else:
            st.info("Ainda não existem registos arquivados.")

    # BOTÃO PARA O ALUNO ASSINALAR FECHO FORMAL DA SESSÃO
    if st.button("🚪 Terminar e Sair por hoje", use_container_width=True):
        if nome_aluno:
            agora_fecho = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            guardar_registo(
                nome=nome_aluno,
                turma=turma_aluno,
                tarefa=st.session_state.tarefa_selecionada,
                data_inicio=st.session_state.data_inicio_tarefa,
                data_reinicio=st.session_state.data_reinicio_sessao,
                ex_id="Saida",
                pergunta="Aluno assinalou término de sessão",
                resposta="Fecho de sessão",
                correta=True,
                tentativas=0,
                tempo_segundos=0,
                tipo_evento="Fecho"
            )
            st.success(f"Trabalho guardado com sucesso às {agora_fecho}! Podes fechar o navegador.")
        else:
            st.warning("Insere o teu nome antes de sair.")

    st.markdown("---")
    st.subheader("🔒 Acesso do Professor")
    senha_docente = st.text_input("Código de acesso docente:", type="password")
    
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
                    mime="text/csv"
                )
                
                # Vista em tempo real com hora de início, reinício e última atividade (fecho)
                with st.expander("📍 Estado Atual dos Alunos (Em Direto)", expanded=True):
                    df_estado = (
                        df_geral.sort_values(by="Data_Hora")
                        .groupby(["Aluno", "Turma", "Tarefa"], as_index=False)
                        .last()
                    )
                    cols_estado = [
                        c for c in [
                            "Aluno", "Turma", "Tarefa", "Data_Inicio_Tarefa", 
                            "Data_Reinicio_Sessao", "Exercicio", "Tipo_Evento", "Data_Hora"
                        ] if c in df_estado.columns
                    ]
                    df_exibir_estado = df_estado[cols_estado].rename(columns={
                        "Data_Inicio_Tarefa": "Hora Início",
                        "Data_Reinicio_Sessao": "Último Reinício",
                        "Data_Hora": "Última Atividade / Fecho",
                        "Exercicio": "Último Exercício"
                    })
                    try:
                        st.dataframe(df_exibir_estado, width="stretch")
                    except TypeError:
                        st.dataframe(df_exibir_estado)

                with st.expander("📋 Histórico Completo de Auditoria", expanded=False):
                    colunas = [
                        c for c in [
                            "Data_Hora", "Data_Inicio_Tarefa", "Data_Reinicio_Sessao", 
                            "Aluno", "Turma", "Tarefa", "Tipo_Evento", "Exercicio", 
                            "Resultado", "Tentativas", "Tempo_Segundos", "Resposta_Dada"
                        ] if c in df_geral.columns
                    ]
                    try:
                        st.dataframe(df_geral[colunas].tail(50), width="stretch")
                    except TypeError:
                        st.dataframe(df_geral[colunas].tail(50))
            else:
                st.info("Ainda não existem registos no ficheiro.")

# ----------------------------------------------------
# 6. ENQUADRAMENTO DA TAREFA E RESUMO TEÓRICO
# ----------------------------------------------------
tarefa_dados = DADOS_TAREFAS[st.session_state.tarefa_selecionada]
lista_exercicios = tarefa_dados["exercicios"]
total_exercicios = len(lista_exercicios)

st.title(f"🎓 {st.session_state.tarefa_selecionada}")
st.caption("Módulo P1: Modelos Matemáticos para a Cidadania | EPDR Grândola")

with st.expander("📖 Guia Teórico e Fórmulas de Apoio (Clica para abrir)", expanded=(st.session_state.indice_pergunta == 0)):
    st.markdown(tarefa_dados["resumo_teorico"])

st.divider()

# Histórico das mensagens do Tutor
for chat in st.session_state.mensagens:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# ----------------------------------------------------
# 7. EXECUÇÃO DOS EXERCÍCIOS
# ----------------------------------------------------
if st.session_state.indice_pergunta >= total_exercicios:
    st.balloons()
    st.success(f"🎉 **Excelente! Concluíste todos os exercícios da {st.session_state.tarefa_selecionada}!**")
    st.info("O teu professor tem acesso à hora de início, reinício e conclusão total desta tarefa.")
else:
    q = lista_exercicios[st.session_state.indice_pergunta]
    progresso = (st.session_state.indice_pergunta) / total_exercicios
    st.progress(progresso, text=f"Progresso: Exercício {st.session_state.indice_pergunta + 1} de {total_exercicios}")

    st.markdown(f"### {q['titulo']}")
    st.markdown(q["enunciado_geral"])
    st.markdown(f"**👉 Pergunta:** {q['pergunta']}")

    if not nome_aluno:
        st.warning("⚠️ Insere o teu nome completo na barra lateral para poderes responder.")
    else:
        with st.form(key=f"form_{st.session_state.tarefa_selecionada}_{q['id']}"):
            resposta_dada = None

            if q["tipo"] == "int":
                resposta_dada = st.number_input("A tua resposta (número inteiro):", step=1, value=0)
            elif q["tipo"] == "float":
                resposta_dada = st.number_input("A tua resposta (valor numérico):", step=0.1, format="%.2f", value=0.0)
            elif q["tipo"] == "choice":
                resposta_dada = st.selectbox("Escolhe a opção correta:", q["opcoes"])

            btn_submeter = st.form_submit_button("Submeter Resposta 🚀")

            if btn_submeter:
                st.session_state.tentativas += 1
                tempo_decorrido = time.time() - st.session_state.tempo_inicio_questao

                # Verificação da Resposta
                acertou = False
                if q["tipo"] == "int":
                    acertou = (int(resposta_dada) == int(q["resposta_correta"]))
                elif q["tipo"] == "float":
                    acertou = abs(float(resposta_dada) - float(q["resposta_correta"])) <= q["tolerancia"]
                elif q["tipo"] == "choice":
                    acertou = (resposta_dada == q["resposta_correta"])

                # Registo no CSV com carimbos temporais completos
                guardar_registo(
                    nome=nome_aluno,
                    turma=turma_aluno,
                    tarefa=st.session_state.tarefa_selecionada,
                    data_inicio=st.session_state.data_inicio_tarefa,
                    data_reinicio=st.session_state.data_reinicio_sessao,
                    ex_id=q["id"],
                    pergunta=q["titulo"],
                    resposta=resposta_dada,
                    correta=acertou,
                    tentativas=st.session_state.tentativas,
                    tempo_segundos=tempo_decorrido,
                    tipo_evento="Conclusão" if (acertou and st.session_state.indice_pergunta + 1 == total_exercicios) else "Resposta"
                )

                if acertou:
                    msg_sucesso = f"✅ **Certo, {nome_aluno}!** Resposta: `{resposta_dada}`. Demoraste {round(tempo_decorrido, 1)}s e usaste {st.session_state.tentativas} tentativa(s)."
                    st.session_state.mensagens.append({"role": "user", "content": f"Submeti: {resposta_dada}"})
                    st.session_state.mensagens.append({"role": "assistant", "content": msg_sucesso})
                    
                    st.session_state.indice_pergunta += 1
                    st.session_state.tentativas = 0
                    st.session_state.tempo_inicio_questao = time.time()
                    st.rerun()
                else:
                    msg_aviso = (
                        f"❌ **A resposta `{resposta_dada}` não está correta.**\n\n"
                        f"💡 **Dica do Tutor:** {q['dica']}\n\n"
                        f"Revê o resumo teórico acima e tenta novamente!"
                    )
                    st.session_state.mensagens.append({"role": "user", "content": f"Submeti: {resposta_dada}"})
                    st.session_state.mensagens.append({"role": "assistant", "content": msg_aviso})
                    st.rerun()