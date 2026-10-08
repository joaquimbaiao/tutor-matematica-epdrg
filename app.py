import os
import csv
import json
from datetime import datetime
import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Tarefa 4 - Matemática para a cidadania",
    page_icon="📐",
    layout="wide"
)

# --- 2. CONFIGURAÇÃO DA API GEMINI (COM FALLBACK ANTI-404) ---
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
elif "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
elif os.environ.get("GEMINI_API_KEY"):
    api_key = os.environ.get("GEMINI_API_KEY")
elif os.environ.get("GOOGLE_API_KEY"):
    api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Chave de API não configurada. Define 'GEMINI_API_KEY' nos Secrets do Streamlit.")
    st.stop()

genai.configure(api_key=api_key)

@st.cache_resource
def obter_modelo():
    preferenciais = [
        "gemini-1.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-pro",
        "gemini-flash-latest"
    ]
    try:
        disponiveis = [
            m.name.replace("models/", "")
            for m in genai.list_models()
            if "generateContent" in m.supported_generation_methods
        ]
        for pref in preferenciais:
            if pref in disponiveis:
                return genai.GenerativeModel(pref)
        if disponiveis:
            return genai.GenerativeModel(disponiveis[0])
    except Exception:
        pass
    return genai.GenerativeModel("gemini-1.5-flash")

# --- 3. GESTÃO DE PERSISTÊNCIA (CSV E SESSÃO JSON) ---
CSV_FILE = "monitorizacao_tarefa4.csv"
CAMPOS_CSV = ["data_hora", "turma", "nome_aluno", "exercicio", "tipo_registo", "detalhes"]
ESTADO_FILE = "estado_alunos.json"

def carregar_estados():
    if os.path.exists(ESTADO_FILE):
        try:
            with open(ESTADO_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def guardar_estado_aluno(chave_aluno, dados):
    estados = carregar_estados()
    estados[chave_aluno] = dados
    with open(ESTADO_FILE, "w", encoding="utf-8") as f:
        json.dump(estados, f, ensure_ascii=False, indent=2)

def registar_interacao_csv(turma, aluno, exercicio, tipo, detalhes):
    ficheiro_existe = os.path.isfile(CSV_FILE)
    resumo = str(detalhes).replace("\n", " ").strip()[:300]
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS_CSV)
        if not ficheiro_existe:
            writer.writeheader()
        writer.writerow({
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "turma": turma,
            "nome_aluno": aluno,
            "exercicio": exercicio,
            "tipo_registo": tipo,
            "detalhes": resumo
        })

# --- 4. BASE DE DADOS DOS EXERCÍCIOS INTEGRAIS (TAREFA 4) ---
exercicios_dados = {
    "Exemplo Guiado: Vencimento Mensal da Catarina": {
        "enunciado": """
**Exemplo:**
A Catarina é casada (2 titulares), tem 1 filho (1 dependente), vive em Braga e aufere mensalmente uma remuneração base de **1256,20 €**. 
Desconta para a Segurança Social (11%) e recebe, por dia, **5,20 €** de subsídio de refeição.

> **Nota:** O valor do subsídio de refeição, por dia, até aos 6 € (inclusive) não está sujeito a tributação.

**Pergunta:** Qual foi o salário líquido da Catarina em abril de 2023, sabendo que trabalhou de segunda a sexta (20 dias úteis considerados)? E o valor total que recebeu no final do mês?
* **Tabela de Retenção de IRS:** Tabela III (Casado, 2 titulares, 1 dependente) $\\rightarrow$ **12,3%**.
""",
        "prompt_contexto": "Verifica: Base = 1256,20 €, Sub. Refeição = 20 x 5,20 = 104,00 €, SS = 1256,20 x 11% = 138,18 €, IRS = 1256,20 x 12,3% = 154,51 €, Salário Líquido = 963,51 €, Valor Total a Receber = 1067,58 €.",
        "solucao": {
            "vencimento_base": 1256.20,
            "subsidio_alimentacao": 104.00,
            "seguranca_social": 138.18,
            "irs": 154.51,
            "outros_descontos": 0.0,
            "liquido": 1067.58
        }
    },
    "Exercício 1: O Caso do Mateus (Açores - Setembro de 2022)": {
        "enunciado": """
**Exercício 1:**
O Mateus é solteiro e não tem filhos, vive nos Açores e aufere mensalmente uma remuneração base de **1956,40 €**. 
Desconta para a segurança social (11%) e recebe, por dia, **5,80 €** de subsídio de refeição.

**Pergunta:** Quanto recebeu em setembro de 2022, sabendo que trabalhou de segunda a sexta (22 dias úteis)?
* **Taxa de Retenção de IRS:** **14,6%**.
""",
        "prompt_contexto": "Verifica: Base = 1956,40 €, Sub. Refeição = 22 x 5,80 = 127,60 €, SS = 1956,40 x 11% = 215,20 €, IRS = 1956,40 x 14,6% = 285,63 €, Valor Total a Receber = 1956,40 + 127,60 - 215,20 - 285,63 = 1583,17 €.",
        "solucao": {
            "vencimento_base": 1956.40,
            "subsidio_alimentacao": 127.60,
            "seguranca_social": 215.20,
            "irs": 285.63,
            "outros_descontos": 0.0,
            "liquido": 1583.17
        }
    },
    "Exercício 2.1: Carlos na Madeira (Fevereiro de 2010)": {
        "enunciado": """
**Exercício 2.1:**
Compara os valores recebidos pelo Carlos. Em **fevereiro de 2010**:
* Solteiro, sem filhos;
* Habitava na Madeira;
* Salário bruto: **845 €**;
* Descontava para a SS (**11%**);
* Subsídio de almoço: **5,20 €/dia**;
* Trabalhou **21 dias** no mês.
* **Taxa de IRS (2010):** **5,67%**.
""",
        "prompt_contexto": "Verifica: Base = 845,00 €, Sub. Almoço = 21 x 5,20 = 109,20 €, SS = 845 x 11% = 92,95 €, IRS = 845 x 5,67% = 47,91 €, Valor Total a Receber = 845 + 109,20 - 92,95 - 47,91 = 813,34 €.",
        "solucao": {
            "vencimento_base": 845.00,
            "subsidio_alimentacao": 109.20,
            "seguranca_social": 92.95,
            "irs": 47.91,
            "outros_descontos": 0.0,
            "liquido": 813.34
        }
    },
    "Exercício 2.2: Carlos em Lisboa (Fevereiro de 2023)": {
        "enunciado": """
**Exercício 2.2:**
Em **fevereiro de 2023**, o Carlos:
* Casado (2 titulares), com 3 filhos;
* Habitava em Lisboa;
* Salário bruto: **975 €**;
* Descontava para a SS (**11%**);
* Subsídio de almoço: **5,90 €/dia**;
* Trabalhou **20 dias** no mês.
* **Taxa de IRS (2023):** **5%**.
""",
        "prompt_contexto": "Verifica: Base = 975,00 €, Sub. Almoço = 20 x 5,90 = 118,00 €, SS = 975 x 11% = 107,25 €, IRS = 975 x 5% = 48,75 €, Valor Total a Receber = 975 + 118,00 - 107,25 - 48,75 = 937,00 €.",
        "solucao": {
            "vencimento_base": 975.00,
            "subsidio_alimentacao": 118.00,
            "seguranca_social": 107.25,
            "irs": 48.75,
            "outros_descontos": 0.0,
            "liquido": 937.00
        }
    },
    "Exercício 3: Mariana na Junta de Freguesia (Exame MACS 2023)": {
        "enunciado": """
**Exercício 3 (Adaptado do Exame de MACS, 1.ª fase, 2023):**
A Mariana é funcionária da Junta de Freguesia de Avelares e aufere um salário bruto de **1700 €**.
Fórmula de cálculo: **SL = SB + SR - SS - RF**
* **SB:** 1700 €;
* **SR:** 5,20 € por cada dia trabalhado (trabalhará **22 dias**);
* **SS:** 11% do salário bruto;
* **RF:** Retenção na fonte por consulta da tabela: intervalo `]1577,00; 1727,00]` com 2 dependentes $\\rightarrow$ **16,1%**.

**Pergunta:** Determina o valor que a Mariana vai receber no próximo mês.
""",
        "prompt_contexto": "Verifica: Base = 1700,00 €, SR = 22 x 5,20 = 114,40 €, SS = 1700 x 11% = 187,00 €, IRS = 1700 x 16,1% = 273,70 €, SL = 1353,70 €.",
        "solucao": {
            "vencimento_base": 1700.00,
            "subsidio_alimentacao": 114.40,
            "seguranca_social": 187.00,
            "irs": 273.70,
            "outros_descontos": 0.0,
            "liquido": 1353.70
        }
    },
    "Exercício 4: Catarina após a Maternidade (Setembro de 2023)": {
        "enunciado": """
**Exercício 4:**
A Catarina, do exemplo inicial, foi mãe em julho de 2023 (passando a ter 2 dependentes). 
Sabendo que a sua remuneração base aumentou **1,3%** em julho e que o subsídio de refeição passou para **6 €**, quanto recebeu em setembro de 2023, sabendo que trabalhou **19 dias**?
* Remuneração base recalculada: $1256,20 \\times 1,013 = 1272,53\\text{ €}$;
* Tabela de IRS (Tabela III, até 1280 €, 2 dependentes) $\\rightarrow$ **11,4%**.
""",
        "prompt_contexto": "Verifica: Base = 1272,53 €, Sub. Refeição = 19 x 6,00 = 114,00 €, SS = 1272,53 x 11% = 139,98 €, IRS = 1272,53 x 11,4% = 145,07 €, Valor Total a Receber = 1101,48 €.",
        "solucao": {
            "vencimento_base": 1272.53,
            "subsidio_alimentacao": 114.00,
            "seguranca_social": 139.98,
            "irs": 145.07,
            "outros_descontos": 0.0,
            "liquido": 1101.48
        }
    },
    "Exercício 5: Carina no Porto (Tabela com Fórmula de Abate)": {
        "enunciado": """
**Exercício 5:**
A Carina recebia, em setembro de 2023, um salário bruto de **800 €**. 
Quanto recebeu nesse mês, sabendo que vivia no Porto, é solteira, não tem filhos, trabalhou 5 dias úteis por semana (**21 dias úteis** em setembro de 2023), recebe **5,50 €** de subsídio de refeição por dia, e descontou para a SS (11%) e para IRS?
* **Cálculo de IRS (2.º semestre de 2023 - Fórmula de Abate):**
  Escalão até 886,57 €: Taxa marginal de 14,5% e parcela a abater de $14,5\\% \\times 2,3 \\times (1093,31 - R)$.
  $\\text{IRS} = (800 \\times 0,145) - [0,145 \\times 2,3 \\times (1093,31 - 800)] = 116,00 - 97,82 = 18,18\\text{ €}$.
""",
        "prompt_contexto": "Verifica: Base = 800,00 €, Sub. Refeição = 21 x 5,50 = 115,50 €, SS = 800 x 11% = 88,00 €, IRS = 18,18 €, Valor Total a Receber = 800 + 115,50 - 88,00 - 18,18 = 809,32 €.",
        "solucao": {
            "vencimento_base": 800.00,
            "subsidio_alimentacao": 115.50,
            "seguranca_social": 88.00,
            "irs": 18.18,
            "outros_descontos": 0.0,
            "liquido": 809.32
        }
    }
}

opcoes_exercicios = list(exercicios_dados.keys())
opcoes_formatadas = [f"👉 {opcoes_exercicios[0]}"] + [f"⚪ {nome}" for nome in opcoes_exercicios[1:]]

# --- 5. INICIALIZAÇÃO DE ESTADO ---
SENHA_CORRETA = st.secrets.get("SENHA_PROFESSOR", "epdr2026")

if "professor_autenticado" not in st.session_state:
    st.session_state["professor_autenticado"] = False

if "indice_exercicio" not in st.session_state:
    st.session_state["indice_exercicio"] = 0

if "valores_folha" not in st.session_state:
    st.session_state["valores_folha"] = {}

# --- 6. BARRA LATERAL ---
with st.sidebar:
    if os.path.exists("Logo.rm.png"):
        st.image("Logo.rm.png", use_container_width=True)
    elif os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("## 🏫 **EPDR Grândola**")

    st.markdown("### **EPDR Grândola**")
    st.markdown("#### **Tarefa 4 - Matemática para a cidadania**")
    
    st.markdown("**Nome do Aluno:**")
    nome_aluno = st.text_input("Nome do Aluno", placeholder="Escreve o teu nome completo", key="input_nome", label_visibility="collapsed")
    
    st.markdown("**Turma:**")
    turma = st.selectbox(
        "Turma",
        ["10º TCP/TRB", "10º A", "10º B", "11º TCP/TRB", "11º A", "12º TCP/TRB", "12º A"],
        index=0,
        key="input_turma",
        label_visibility="collapsed"
    )

    # --- BOTÕES DE GESTÃO DE SESSÃO DO ALUNO ---
    st.markdown("##### ⏱️ Gestão da Sessão de Trabalho")
    col_sessao1, col_sessao2 = st.columns(2)
    chave_aluno = f"{turma}_{nome_aluno.strip().lower()}" if nome_aluno.strip() else None

    with col_sessao1:
        if st.button("💾 Guardar e Fechar", use_container_width=True, help="Guarda o progresso para continuares em casa ou na próxima aula."):
            if not chave_aluno:
                st.warning("⚠️ Insere o teu nome antes de guardar.")
            else:
                dados_progresso = {
                    "turma": turma,
                    "nome_aluno": nome_aluno.strip(),
                    "indice_exercicio": st.session_state["indice_exercicio"],
                    "valores_folha": st.session_state["valores_folha"],
                    "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                guardar_estado_aluno(chave_aluno, dados_progresso)
                registar_interacao_csv(turma, nome_aluno, opcoes_exercicios[st.session_state["indice_exercicio"]], "Sessao_Fechada", "Aluno guardou o estado da aula.")
                st.success("Sessão guardada com sucesso! Até à próxima aula.")

    with col_sessao2:
        if st.button("🔄 Retomar Sessão", use_container_width=True, help="Recupera o último exercício e contas guardadas."):
            if not chave_aluno:
                st.warning("⚠️ Escreve o teu nome completo para recuperar.")
            else:
                estados = carregar_estados()
                if chave_aluno in estados:
                    dados_recup = estados[chave_aluno]
                    st.session_state["indice_exercicio"] = dados_recup.get("indice_exercicio", 0)
                    st.session_state["valores_folha"] = dados_recup.get("valores_folha", {})
                    st.success("Sessão anterior recuperada com sucesso!")
                    st.rerun()
                else:
                    st.info("Nenhuma sessão anterior encontrada com este nome.")

    st.markdown("---")
    st.markdown("### 📍 Lista de Exercícios")

    opcoes_menu = opcoes_formatadas + ["🔒 Área do Professor"]
    
    # Índice atual selecionado na navegação
    idx_padrao = st.session_state["indice_exercicio"] if st.session_state["indice_exercicio"] < len(opcoes_formatadas) else 0

    navegacao = st.radio(
        "Menu",
        opcoes_menu,
        index=idx_padrao,
        key="radio_navegacao",
        label_visibility="collapsed"
    )

    if navegacao in opcoes_formatadas:
        st.session_state["indice_exercicio"] = opcoes_formatadas.index(navegacao)

# --- 7. ÁREA PROTEGIDA DO PROFESSOR ---
if navegacao == "🔒 Área do Professor":
    st.title("🔒 Área de Monitorização Docente")
    st.caption("Acesso reservado ao professor da disciplina.")

    if not st.session_state["professor_autenticado"]:
        with st.form("form_login_prof"):
            senha_digitada = st.text_input("Introduz a palavra-passe de acesso:", type="password")
            entrar = st.form_submit_button("Entrar no Painel", use_container_width=True)
            
            if entrar:
                if senha_digitada == SENHA_CORRETA:
                    st.session_state["professor_autenticado"] = True
                    st.rerun()
                else:
                    st.error("Palavra-passe incorreta. Acesso negado.")
    else:
        col_t, col_btn = st.columns([4, 1])
        with col_t:
            st.success("Sessão docente ativa.")
        with col_btn:
            if st.button("Terminar Sessão", use_container_width=True):
                st.session_state["professor_autenticado"] = False
                st.rerun()

        st.markdown("---")

        if os.path.isfile(CSV_FILE):
            import pandas as pd
            df = pd.read_csv(CSV_FILE)
            
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Total de Registos", len(df))
            col_m2.metric("Alunos Distintos", df["nome_aluno"].nunique())
            col_m3.metric("Exercícios Submetidos", df["exercicio"].nunique())
            
            st.markdown("---")
            turma_filtro = st.multiselect("Filtrar por Turma:", options=df["turma"].unique(), default=df["turma"].unique())
            df_filtrado = df[df["turma"].isin(turma_filtro)]
            
            st.dataframe(df_filtrado, use_container_width=True)

            with open(CSV_FILE, "rb") as f:
                st.download_button(
                    label="📥 Descarregar Folha de Monitorização (CSV)",
                    data=f,
                    file_name=f"monitorizacao_alunos_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("Ainda não existem registos de submissões guardados.")
            
    st.stop()

# --- 8. ÁREA DO ALUNO ---
indice_escolhido = st.session_state["indice_exercicio"]
exercicio_atual = opcoes_exercicios[indice_escolhido]
dados_ex = exercicios_dados[exercicio_atual]

st.title("Tarefa 4 - Matemática para a cidadania")
st.markdown(f"### `{exercicio_atual}`")
st.markdown(dados_ex["enunciado"])

# --- PASSO 1: FOTOGRAFIA DO CADERNO & TUTOR IA ---
st.markdown("---")
st.markdown("## 📸 Passo 1: Faz os cálculos no caderno e tira uma fotografia")
st.caption("Usa o caderno para estruturar o raciocínio. O Tutor lê as tuas contas e valida os passos matemáticos.")

col_cam, col_upload = st.columns([1.1, 0.9])

with col_cam:
    st.markdown("📷 **Fotografar a resolução no caderno**")
    foto_cam = st.camera_input("Tirar foto", label_visibility="collapsed", key=f"cam_{indice_escolhido}")

with col_upload:
    st.markdown("📁 **Ou envia ficheiro da galeria**")
    foto_upload = st.file_uploader(
        "Upload",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed",
        key=f"up_{indice_escolhido}"
    )

imagem_final = foto_cam if foto_cam is not None else foto_upload

if imagem_final is not None:
    img = Image.open(imagem_final)
    st.image(img, caption="A tua folha de cálculos", use_container_width=True)
    
    if st.button("🔍 Pedir Análise ao Tutor IA", type="primary", use_container_width=True):
        if not nome_aluno.strip():
            st.warning("⚠️ Por favor, escreve o teu nome completo na barra lateral à esquerda.")
        else:
            with st.spinner("O Tutor IA está a avaliar os teus cálculos manuscritos..."):
                try:
                    model = obter_modelo()
                    prompt = (
                        f"És um tutor de Matemática para a Cidadania na EPDR Grândola.\n"
                        f"Aluno: {nome_aluno} (Turma: {turma})\n"
                        f"Exercício: {exercicio_atual}\n"
                        f"Enunciado: {dados_ex['enunciado']}\n"
                        f"Valores oficiais de referência: {dados_ex['prompt_contexto']}\n\n"
                        "Analisa a folha de cálculos do aluno presente na imagem:\n"
                        "1. Confere cada operação aritmética (dias úteis, percentagem da SS, escalão e percentagem de IRS, total líquido).\n"
                        "2. Se detetares algum engano, indica a linha exata e orienta o aluno pedagogicamente para a correção.\n"
                        "3. Se as contas estiverem corretas, confirma o sucesso e convida o aluno a registar os valores na Folha de Vencimento no Passo 2 abaixo."
                    )
                    response = model.generate_content([prompt, img])
                    feedback_ia = response.text
                    
                    st.success("Análise do Tutor concluída!")
                    st.markdown(feedback_ia)
                    
                    registar_interacao_csv(turma, nome_aluno, exercicio_atual, "Analise_IA", feedback_ia)
                except Exception as e:
                    st.error(f"Erro ao processar imagem com a IA: {e}")

# --- PASSO 2: PREENCHIMENTO DA FOLHA DE VENCIMENTO ---
st.markdown("---")
st.markdown("## ✍️ Passo 2: Preenchimento da Folha de Vencimento")
st.caption("Transfere os valores calculados para a folha e carrega em validar para conferir com a chave oficial.")

valores_salvos = st.session_state["valores_folha"].get(exercicio_atual, {})

with st.form(key=f"form_folha_{indice_escolhido}"):
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("#### **Recebe (€)**")
        v_base = st.number_input("Remuneração Base (€):", min_value=0.0, value=float(valores_salvos.get("base", 0.0)), format="%.2f", step=0.01)
        v_sub_alim = st.number_input("Subsídio de Refeição (€):", min_value=0.0, value=float(valores_salvos.get("sub_alim", 0.0)), format="%.2f", step=0.01)
        total_rec = v_base + v_sub_alim
        st.info(f"**Total a Receber Ilíquido:** {total_rec:.2f} €")

    with c2:
        st.markdown("#### **Desconta (€)**")
        v_ss = st.number_input("Contribuição para a Segurança Social (SS) (€):", min_value=0.0, value=float(valores_salvos.get("ss", 0.0)), format="%.2f", step=0.01)
        v_irs = st.number_input("Retenção na Fonte (IRS) (€):", min_value=0.0, value=float(valores_salvos.get("irs", 0.0)), format="%.2f", step=0.01)
        v_outros = st.number_input("Outros Descontos (€):", min_value=0.0, value=float(valores_salvos.get("outros", 0.0)), format="%.2f", step=0.01)
        total_desc = v_ss + v_irs + v_outros
        st.warning(f"**Total de Descontos:** {total_desc:.2f} €")

    st.markdown("---")
    v_liquido = st.number_input("💰 **Valor Total a Receber no Final do Mês (€):**", min_value=0.0, value=float(valores_salvos.get("liquido", 0.0)), format="%.2f", step=0.01)
    
    submeter_folha = st.form_submit_button("✅ Validar Folha de Vencimento", use_container_width=True)

if submeter_folha:
    if not nome_aluno.strip():
        st.warning("⚠️ Insere o teu nome completo na barra lateral para poderes validar a folha.")
    else:
        # Guarda na memória interna do browser
        st.session_state["valores_folha"][exercicio_atual] = {
            "base": v_base,
            "sub_alim": v_sub_alim,
            "ss": v_ss,
            "irs": v_irs,
            "outros": v_outros,
            "liquido": v_liquido
        }
        
        sol = dados_ex.get("solucao")
        if sol:
            erros = []
            if abs(v_base - sol["vencimento_base"]) > 0.05:
                erros.append(f"Remuneração Base incorreta (esperado: {sol['vencimento_base']:.2f} €).")
            if abs(v_sub_alim - sol["subsidio_alimentacao"]) > 0.05:
                erros.append(f"Subsídio de Refeição incorreto (esperado: {sol['subsidio_alimentacao']:.2f} €).")
            if abs(v_ss - sol["seguranca_social"]) > 0.05:
                erros.append(f"Segurança Social incorreta (esperado: {sol['seguranca_social']:.2f} €).")
            if abs(v_irs - sol["irs"]) > 0.05:
                erros.append(f"Retenção de IRS incorreta (esperado: {sol['irs']:.2f} €).")
            if abs(v_liquido - sol["liquido"]) > 0.05:
                erros.append(f"Valor a Receber incorreto (esperado: {sol['liquido']:.2f} €).")

            if not erros:
                st.success(f"🎉 Excelente, {nome_aluno}! Todos os campos da folha de vencimento estão rigorosamente corretos!")
                status = "Correto_100%"
            else:
                st.error("A folha apresenta divergências:")
                for e in erros:
                    st.write(f"- {e}")
                status = f"Erros_{len(erros)}"
        else:
            status = "Sem_Chave"

        detalhe_registo = f"Base:{v_base:.2f}|Sub:{v_sub_alim:.2f}|SS:{v_ss:.2f}|IRS:{v_irs:.2f}|Liq:{v_liquido:.2f}|Status:{status}"
        registar_interacao_csv(turma, nome_aluno, exercicio_atual, "Folha_Vencimento", detalhe_registo)
