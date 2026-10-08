import streamlit as st
import pandas as pd
from PIL import Image
import io
import os
from google import genai

# ----------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA
# ----------------------------------------------------
st.set_page_config(
    page_title="Tutor MACS - Folha de Vencimento Dinâmica",
    page_icon="💶",
    layout="wide"
)

# Inicializar cliente Gemini através dos Secrets
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", None))
client = genai.Client(api_key=api_key) if api_key else None

# ----------------------------------------------------
# 2. BASE DE DADOS DOS EXERCÍCIOS DA TAREFA 4
# ----------------------------------------------------
EXERCICIOS_T4 = [
    {
        "id": "T4_Exemplo",
        "titulo": "Exemplo Guiado: Vencimento Mensal com ADSE",
        "enunciado": """
        > O funcionário aufere uma **Remuneração Base de 1 988,35 €**.  
        > Trabalhou **20 dias úteis** com subsídio de alimentação de **5,20 €/dia**.  
        > Está sujeito a:  
        > * **11%** para a Segurança Social;  
        > * **20,4%** de retenção na fonte de IRS;  
        > * **3,5%** de contribuição para a ADSE.
        """,
        "base": 1988.35,
        "sub_ref": 104.00,  # 20 * 5.20
        "irs": 405.62,      # 1988.35 * 0.204
        "ss": 218.72,       # 1988.35 * 0.11
        "adse": 69.59,      # 1988.35 * 0.035
        "tem_adse": True,
        "dicas": {
            "sub_ref": "Multiplica os 20 dias pelos 5,20 €/dia (20 × 5,20).",
            "irs": "Calcula 20,4% sobre a remuneração base (1 988,35 × 0,204).",
            "ss": "Aplica os 11% sobre a remuneração base (1 988,35 × 0,11).",
            "adse": "Aplica os 3,5% sobre a remuneração base (1 988,35 × 0,035)."
        }
    },
    {
        "id": "T4_Ex1_Mateus",
        "titulo": "Exercício 1: O Caso do Mateus (Açores - Setembro de 2022)",
        "enunciado": """
        > O Mateus vive nos Açores, é solteiro e não tem filhos.  
        > Aufere uma remuneração base mensal de **1 956,40 €**.  
        > Em setembro de 2022 trabalhou **22 dias úteis**, recebendo um subsídio de refeição de **5,80 €/dia**.  
        > Sabendo que está sujeito a uma taxa de retenção de IRS de **14,6%** e desconta **11%** para a Segurança Social:
        """,
        "base": 1956.40,
        "sub_ref": 127.60,  # 22 * 5.80
        "irs": 285.63,      # 1956.40 * 0.146
        "ss": 215.20,       # 1956.40 * 0.11
        "adse": 0.0,
        "tem_adse": False,
        "dicas": {
            "sub_ref": "Multiplica os 22 dias pelos 5,80 €/dia (22 × 5,80).",
            "irs": "Multiplica a remuneração base por 0,146 (1 956,40 × 0,146).",
            "ss": "Multiplica a remuneração base por 0,11 (1 956,40 × 0,11)."
        }
    },
    {
        "id": "T4_Ex2A_Carlos2010",
        "titulo": "Exercício 2.1: Carlos na Madeira (Fevereiro de 2010)",
        "enunciado": """
        > Em fevereiro de 2010, o Carlos auferia um salário bruto de **845,00 €**.  
        > Trabalhou **21 dias úteis** e recebeu **5,20 €/dia** de subsídio de almoço.  
        > Descontava **11%** para a Segurança Social e a sua taxa de retenção na fonte de IRS era de **5,67%**.
        """,
        "base": 845.00,
        "sub_ref": 109.20,  # 21 * 5.20
        "irs": 47.91,       # 845.00 * 0.0567
        "ss": 92.95,        # 845.00 * 0.11
        "adse": 0.0,
        "tem_adse": False,
        "dicas": {
            "sub_ref": "Multiplica 21 dias por 5,20 €/dia (21 × 5,20).",
            "irs": "Aplica a taxa de 5,67% sobre o salário bruto (845 × 0,0567).",
            "ss": "Aplica os 11% sobre o salário bruto (845 × 0,11)."
        }
    },
    {
        "id": "T4_Ex2B_Carlos2023",
        "titulo": "Exercício 2.2: Carlos em Lisboa (Fevereiro de 2023)",
        "enunciado": """
        > Em fevereiro de 2023, o Carlos auferia uma remuneração bruta de **975,00 €**.  
        > Trabalhou **20 dias úteis** e recebeu **5,90 €/dia** de subsídio de almoço.  
        > Descontava **11%** para a Segurança Social e a sua taxa de IRS era de **5,0%**.
        """,
        "base": 975.00,
        "sub_ref": 118.00,  # 20 * 5.90
        "irs": 48.75,       # 975.00 * 0.05
        "ss": 107.25,       # 975.00 * 0.11
        "adse": 0.0,
        "tem_adse": False,
        "dicas": {
            "sub_ref": "Multiplica 20 dias por 5,90 €/dia (20 × 5,90).",
            "irs": "Aplica a taxa de 5% sobre a remuneração base (975 × 0,05).",
            "ss": "Aplica a taxa de 11% sobre a remuneração base (975 × 0,11)."
        }
    },
    {
        "id": "T4_Ex3_Mariana",
        "titulo": "Exercício 3: Mariana na Junta de Freguesia (Exame MACS 2023)",
        "enunciado": """
        > A Mariana é casada (única titular de rendimentos), tem 2 filhos e aufere **1 700,00 €** brutos.  
        > Consultando a tabela de retenção de IRS aplicável, a sua taxa de retenção é de **16,1%**.  
        > Trabalhou **22 dias úteis** com subsídio de alimentação de **5,20 €/dia** e desconta **11%** para a SS.
        """,
        "base": 1700.00,
        "sub_ref": 114.40,  # 22 * 5.20
        "irs": 273.70,      # 1700.00 * 0.161
        "ss": 187.00,       # 1700.00 * 0.11
        "adse": 0.0,
        "tem_adse": False,
        "dicas": {
            "sub_ref": "Multiplica 22 dias por 5,20 €/dia (22 × 5,20).",
            "irs": "Calcula 16,1% sobre a remuneração base (1 700 × 0,161).",
            "ss": "Calcula 11% sobre a remuneração base (1 700 × 0,11)."
        }
    },
    {
        "id": "T4_Ex4_Catarina",
        "titulo": "Exercício 4: Catarina após a Maternidade (Setembro de 2023)",
        "enunciado": """
        > A Catarina auferia 1 256,20 € e teve um **aumento salarial de 1,3%**, passando o seu salário base para **1 272,53 €**.  
        > É casada (2 titulares) e tem 2 dependentes (consultando a Tabela III a taxa de IRS é **11,4%**).  
        > Em setembro de 2023 trabalhou **19 dias** e recebeu **6,00 €/dia** de subsídio de almoço. Desconta **11%** para a SS.
        """,
        "base": 1272.53,
        "sub_ref": 114.00,  # 19 * 6.00
        "irs": 145.07,      # 1272.53 * 0.114
        "ss": 139.98,       # 1272.53 * 0.11
        "adse": 0.0,
        "tem_adse": False,
        "dicas": {
            "sub_ref": "Multiplica 19 dias por 6,00 €/dia (19 × 6,00).",
            "irs": "Aplica os 11,4% sobre o novo salário de 1 272,53 € (1 272,53 × 0,114).",
            "ss": "Aplica os 11% sobre o novo salário base (1 272,53 × 0,11)."
        }
    },
    {
        "id": "T4_Ex5_Carina",
        "titulo": "Exercício 5: Carina no Porto (Tabela com Fórmula de Abate)",
        "enunciado": """
        > A Carina vive no Porto, é solteira e não tem filhos. O seu vencimento base é de **800,00 €**.  
        > Trabalhou **21 dias úteis** e recebeu subsídio de refeição de **5,50 €/dia**.  
        > Desconta **11%** para a Segurança Social.  
        > Na Tabela I do 2.º semestre de 2023: Taxa Marginal = **14,50%** e Parcela a Abater = **97,82 €**  
        > *(Imposto a reter = 800 × 0,145 - 97,82 = 18,18 €)*.
        """,
        "base": 800.00,
        "sub_ref": 115.50,  # 21 * 5.50
        "irs": 18.18,       # (800 * 0.145) - 97.82
        "ss": 88.00,        # 800 * 0.11
        "adse": 0.0,
        "tem_adse": False,
        "dicas": {
            "sub_ref": "Multiplica 21 dias por 5,50 €/dia (21 × 5,50).",
            "irs": "Calcula (800 × 0,145) e subtrai a parcela de 97,82 €.",
            "ss": "Aplica os 11% sobre os 800 € (800 × 0,11)."
        }
    }
]

# ----------------------------------------------------
# 3. GESTÃO DE ESTADO
# ----------------------------------------------------
if "indice_ex" not in st.session_state:
    st.session_state.indice_ex = 0
if "resolvidos" not in st.session_state:
    st.session_state.resolvidos = {}

# ----------------------------------------------------
# 4. BARRA LATERAL (NAVEGAÇÃO E ALUNO)
# ----------------------------------------------------
with st.sidebar:
    st.title("EPDR Grândola")
    st.markdown("### Módulo P1 — MACS")
    nome_aluno = st.text_input("Nome do Aluno:", placeholder="Escreve o teu nome completo").strip()
    turma_aluno = st.selectbox("Turma:", ["10º TCP/TRB", "10º TPA/TOE"])
    
    st.markdown("---")
    st.markdown("### 📍 Lista de Exercícios")
    for idx, ex in enumerate(EXERCICIOS_T4):
        status = "✅" if ex["id"] in st.session_state.resolvidos else ("👉" if idx == st.session_state.indice_ex else "⚪")
        if st.button(f"{status} {ex['titulo']}", key=f"nav_{idx}", use_container_width=True):
            st.session_state.indice_ex = idx
            st.rerun()

# ----------------------------------------------------
# 5. APOIO TEÓRICO E TABELAS NO TOPO (VISÍVEIS)
# ----------------------------------------------------
st.title("💶 Tarefa 4: Matemática nos Salários")
st.caption("Aprende a calcular a folha de vencimento passo a passo.")

with st.expander("📖 Consulta Obrigatória: Fórmulas Legais e Tabelas Oficiais de IRS", expanded=True):
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("""
        **Regras de Cálculo:**
        * **Segurança Social (SS):** $\\text{Remuneração Base} \\times 0,11$ ($11\%$)
        * **Subsídio de Refeição:** $\\text{Dias Trabalhados} \\times \\text{Valor Diário}$
        * **Salário Líquido:** $\\text{Remuneração Base} - \\text{Descontos (SS + IRS + ADSE)}$
        * **Valor Final a Receber:** $\\text{Salário Líquido} + \\text{Subsídio de Refeição}$
        """)
    with col_t2:
        st.markdown("""
        **Tabela de Apoio — Casado 2 Titulares (1.º Sem. 2023):**
        * Até 1 280,00 € (1 dep.): **12,3%**
        * Até 1 280,00 € (2 dep.): **11,4%**
        * Até 1 380,00 € (2 dep.): **12,5%**
        * Até 1 727,00 € (2 dep., 1 tit.): **16,1%**
        """)

st.markdown("---")

# ----------------------------------------------------
# 6. EXERCÍCIO ATUAL
# ----------------------------------------------------
ex_atual = EXERCICIOS_T4[st.session_state.indice_ex]

st.subheader(f"📍 {ex_atual['titulo']}")
st.markdown(ex_atual["enunciado"])

# ----------------------------------------------------
# 7. WIDGET DA CÂMARA COM O TUTOR IA
# ----------------------------------------------------
st.markdown("### 📸 Passo 1: Faz os cálculos no caderno e tira uma fotografia")
st.caption("Usa o caderno para estruturar o raciocínio. O Tutor lê as tuas contas e diz-te se estás no bom caminho.")

col_cam, col_up = st.columns([1, 1])
with col_cam:
    foto_cam = st.camera_input("📷 Fotografar a resolução no caderno", key=f"cam_{ex_atual['id']}")
with col_up:
    foto_file = st.file_uploader("📁 Ou envia ficheiro da galeria", type=["jpg", "png", "jpeg"], key=f"up_{ex_atual['id']}")

imagem_aluno = foto_cam or foto_file

if imagem_aluno is not None:
    img_preview = Image.open(imagem_aluno)
    st.image(img_preview, caption="A tua folha de cálculos", width=320)
    
    if st.button("🔍 Pedir Análise ao Tutor IA", key=f"btn_ia_{ex_atual['id']}", use_container_width=True):
        if not client:
            st.warning("Chave GEMINI_API_KEY não configurada nos Secrets do Streamlit.")
        else:
            with st.spinner("O Tutor está a ler o teu caderno e a rever as tuas contas..."):
                try:
                    img_bytes = imagem_aluno.getvalue()
                    img_pil = Image.open(io.BytesIO(img_bytes))
                    
                    prompt_tutor = f"""
                    És o Tutor Pedagógico de Matemática do Ensino Profissional (EPDRG).
                    Estás a analisar a foto do caderno de um aluno para o seguinte exercício de vencimento:
                    - Remuneração Base: {ex_atual['base']} €
                    - Subsídio de Refeição esperado: {ex_atual['sub_ref']} €
                    - Retenção IRS esperada: {ex_atual['irs']} €
                    - Desconto SS esperado: {ex_atual['ss']} €
                    - ADSE esperada: {ex_atual['adse']} €
                    
                    DIRETIVAS OBRIGATÓRIAS:
                    1. NUNCA dês a resposta numérica final nem faças as contas diretas pelo aluno.
                    2. Se o aluno acertou nos passos, dá-lhe os parabéns e diz para preencher a folha abaixo.
                    3. Se houver um engano em alguma parcela, aponta especificamente a linha com o erro (ex: 'Na conta do subsídio de refeição reparaste nos dias?' ou 'A taxa de IRS foi aplicada corretamente sobre o valor base?').
                    4. Mantém um tom próximo, construtivo e socrático.
                    """
                    
                    resp = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=[prompt_tutor, img_pil]
                    )
                    st.info("💡 **Feedback do Tutor:**")
                    st.markdown(resp.text)
                except Exception as err:
                    st.error(f"Erro ao processar imagem com a IA: {err}")

st.markdown("---")

# ----------------------------------------------------
# 8. FOLHA DE CÁLCULO DINÂMICA (ENTRADA DE DADOS)
# ----------------------------------------------------
st.markdown("### ✍️ Passo 2: Preenchimento da Folha de Vencimento")
st.write("Coloca os teus valores calculados em cada linha correspondente:")

col_rubrica, col_rec, col_desc = st.columns([3, 2, 2])

with col_rubrica:
    st.markdown("#### Rubrica")
    st.markdown("**Remuneração Base**")
    st.markdown("**Subsídio de Refeição**")
    st.markdown("**Retenção na Fonte (IRS)**")
    st.markdown("**Contribuição para a Segurança Social (11%)**")
    if ex_atual["tem_adse"]:
        st.markdown("**Contribuição para a ADSE (3,5%)**")

with col_rec:
    st.markdown("#### Recebe (€)")
    st.number_input("Base", value=ex_atual["base"], disabled=True, key=f"base_in_{ex_atual['id']}", label_visibility="collapsed")
    in_sub = st.number_input("Subsídio Refeição (€)", value=0.00, step=0.1, format="%.2f", key=f"sub_in_{ex_atual['id']}")
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
    if ex_atual["tem_adse"]:
        st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

with col_desc:
    st.markdown("#### Desconta (€)")
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
    in_irs = st.number_input("Retenção IRS (€)", value=0.00, step=0.1, format="%.2f", key=f"irs_in_{ex_atual['id']}")
    in_ss = st.number_input("Segurança Social (€)", value=0.00, step=0.1, format="%.2f", key=f"ss_in_{ex_atual['id']}")
    if ex_atual["tem_adse"]:
        in_adse = st.number_input("ADSE (€)", value=0.00, step=0.1, format="%.2f", key=f"adse_in_{ex_atual['id']}")
    else:
        in_adse = 0.0

st.markdown("---")

if st.button("Validar Linha a Linha e Fechar Recibo 🚀", key=f"btn_val_{ex_atual['id']}", use_container_width=True):
    erros = []
    
    if abs(in_sub - ex_atual["sub_ref"]) > 0.15:
        erros.append(f"❌ **Subsídio de Refeição:** O valor introduzido não está correto. Dica: {ex_atual['dicas']['sub_ref']}")
    if abs(in_irs - ex_atual["irs"]) > 0.15:
        erros.append(f"❌ **Retenção na Fonte (IRS):** O valor introduzido não está correto. Dica: {ex_atual['dicas']['irs']}")
    if abs(in_ss - ex_atual["ss"]) > 0.15:
        erros.append(f"❌ **Segurança Social (11%):** O valor introduzido não está correto. Dica: {ex_atual['dicas']['ss']}")
    if ex_atual["tem_adse"] and abs(in_adse - ex_atual["adse"]) > 0.15:
        erros.append(f"❌ **Contribuição ADSE (3,5%):** O valor introduzido não está correto. Dica: {ex_atual['dicas']['adse']}")

    if not erros:
        st.session_state.resolvidos[ex_atual["id"]] = True
        
        total_descontos = in_irs + in_ss + in_adse
        salario_liquido = ex_atual["base"] - total_descontos
        valor_final = salario_liquido + in_sub
        
        st.success("🎯 **Excelente trabalho! Todos os cálculos parciais foram validados com rigor!**")
        
        linhas_rubrica = ["Remuneração base", "Subsídio de refeição", "Retenção na fonte (IRS)", "Contribuição para a SS"]
        linhas_recebe = [f"{ex_atual['base']:.2f}", f"{in_sub:.2f}", "-", "-"]
        linhas_desconta = ["-", "-", f"{in_irs:.2f}", f"{in_ss:.2f}"]
        
        if ex_atual["tem_adse"]:
            linhas_rubrica.append("Contribuição para a ADSE")
            linhas_recebe.append("-")
            linhas_desconta.append(f"{in_adse:.2f}")
            
        linhas_rubrica.extend(["---", "Salário líquido", "Valor recebido no final do mês"])
        linhas_recebe.extend(["---", f"{salario_liquido:.2f}", f"{valor_final:.2f}"])
        linhas_desconta.extend(["---", "-", "-"])
        
        df_recibo = pd.DataFrame({
            "Rubrica": linhas_rubrica,
            "Recebe (€)": linhas_recebe,
            "Desconta (€)": linhas_desconta
        })
        
        st.markdown("### 📋 Recibo Consolidado do Vencimento")
        st.table(df_recibo)
        
        if st.session_state.indice_ex + 1 < len(EXERCICIOS_T4):
            if st.button("Avançar para o Próximo Exercício ➡️", use_container_width=True):
                st.session_state.indice_ex += 1
                st.rerun()
        else:
            st.balloons()
            st.success("🏆 Concluíste com sucesso todos os exercícios da Tarefa 4!")
    else:
        st.warning("⚠️ Foram detetados enganos nos cálculos. Analisa as pistas abaixo e tenta de novo:")
        for e in erros:
            st.markdown(e)
