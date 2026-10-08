import streamlit as st
import pandas as pd
from PIL import Image
import os
from google import genai
from google.genai import types

# ----------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA
# ----------------------------------------------------
st.set_page_config(
    page_title="Tutor MACS - Folha de Vencimento com IA",
    page_icon="💶",
    layout="wide"
)

# Inicializar cliente Gemini através dos Secrets
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", None))
client = genai.Client(api_key=api_key) if api_key else None

st.title("💶 Tarefa 4: Matemática nos Salários")
st.subheader("Folha de Vencimento Dinâmica com Tutor de Visão")

# ----------------------------------------------------
# 2. CONSULTA DE APOIO (TABELAS DE RETENÇÃO)
# ----------------------------------------------------
with st.expander("📖 Consulta de Apoio: Fórmulas e Tabelas de IRS", expanded=False):
    st.markdown("""
    * **Segurança Social (SS):** $\\text{Salário Bruto} \\times 0,11$
    * **Retenção na Fonte (IRS):** $\\text{Salário Bruto} \\times \\text{Taxa de IRS}$
    * **Subsídio de Refeição:** $\\text{Dias Trabalhados} \\times \\text{Valor Diário}$
    * **Salário Líquido:** $\\text{Remuneração Base} - \\text{Descontos (IRS + SS + ADSE)}$
    * **Valor Recebido no Final do Mês:** $\\text{Salário Líquido} + \\text{Subsídio de Refeição}$
    """)
    dados_irs = {
        "Remuneração Mensal (€)": ["Até 1051,00", "Até 1113,00", "Até 1194,00", "Até 1280,00", "Até 1380,00", "Até 1988,35"],
        "Não Casado (0 Dep.)": ["14,0%", "15,0%", "16,0%", "17,5%", "19,0%", "20,4%"]
    }
    st.table(pd.DataFrame(dados_irs))

st.markdown("---")

# ----------------------------------------------------
# 3. ENUNCIADO DO EXERCÍCIO
# ----------------------------------------------------
st.markdown("""
### 📍 Caso Prático: Vencimento Mensal
> O trabalhador aufere uma **Remuneração Base de 1 988,35 €**.  
> Trabalhou **20 dias úteis** com subsídio de alimentação de **5,20 €/dia**.  
> Está sujeito a:
> * **11%** para a Segurança Social;
> * **20,4%** de taxa de IRS;
> * **3,5%** para a ADSE.  
""")

# ----------------------------------------------------
# 4. SECÇÃO MULTIMODAL: FOTOGRAFIA DO CADERNO
# ----------------------------------------------------
st.markdown("### 📸 Passo 1: Faz os cálculos no caderno e valida aqui")
st.caption("Faz as contas na tua folha de papel. Depois, tira uma fotografia para receberes feedback do tutor antes de preencheres a folha final.")

col_cam, col_upload = st.columns(2)
with col_cam:
    foto_cam = st.camera_input("📷 Tirar foto diretamente ao caderno")
with col_upload:
    foto_file = st.file_uploader("📁 Ou carregar imagem da galeria", type=["jpg", "jpeg", "png"])

imagem_submetida = foto_cam or foto_file

if imagem_submetida:
    st.image(imagem_submetida, caption="Resolução fotografada", width=350)
    
    if st.button("🔍 Analisar Resolução do Caderno", use_container_width=True):
        if not client:
            st.error("⚠️ Chave de API não configurada. Define 'GEMINI_API_KEY' nos Secrets do Streamlit.")
        else:
            with st.spinner("O Tutor está a ler o teu caderno e a rever as contas..."):
                try:
                    img = Image.open(imagem_submetida)
                    prompt_sistema = """
                    És o Tutor Pedagógico de Matemática do Ensino Profissional (EPDRG).
                    Estás a analisar a foto do caderno de um aluno sobre o seguinte problema de salários:
                    - Salário base: 1988,35 €
                    - Subsídio refeição: 20 dias * 5,20 € = 104,00 €
                    - IRS: 1988,35 * 20,4% = 405,62 €
                    - SS: 1988,35 * 11% = 218,72 €
                    - ADSE: 1988,35 * 3,5% = 69,59 €
                    - Salário Líquido: 1988,35 - (405,62 + 218,72 + 69,59) = 1294,42 €
                    - Valor Final: 1294,42 + 104,00 = 1398,42 €

                    INSTRUÇÕES OBRIGATÓRIAS:
                    1. Trata o aluno com proximidade e incentivo.
                    2. NUNCA dês a resposta final ou o resultado numérico corrigido se ele tiver errado.
                    3. Se houver um erro, identifica a linha ou operação com falha (ex: "Reparei que na conta da Segurança Social multiplicaste por 0,011 em vez de 0,11").
                    4. Se as contas estiverem corretas, elogia o rigor e diz-lhe para transpor os números para a tabela abaixo.
                    5. Se a caligrafia estiver ilegível ou faltarem partes, pede com simpatia para focar melhor a imagem.
                    """
                    
                    resposta = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[prompt_sistema, img]
                    )
                    
                    st.info("💡 **Feedback do Tutor:**")
                    st.markdown(resposta.text)
                except Exception as e:
                    st.error(f"Erro na análise visual: {e}")

st.markdown("---")

# ----------------------------------------------------
# 5. FOLHA DE VENCIMENTO DINÂMICA (SUBMISSÃO FINAL)
# ----------------------------------------------------
st.markdown("### ✍️ Passo 2: Preenchimento da Folha de Vencimento")

col_desc, col_recebe, col_desconta = st.columns([3, 2, 2])

with col_desc:
    st.markdown("### Rubrica")
    st.markdown("**Remuneração Base**")
    st.markdown("**Subsídio de Refeição** (20 dias × 5,20 €)")
    st.markdown("**Retenção na Fonte (IRS)** (20,4%)")
    st.markdown("**Contribuição para a Segurança Social** (11%)")
    st.markdown("**Contribuição para a ADSE** (3,5%)")

with col_recebe:
    st.markdown("### Recebe (€)")
    rem_base = st.number_input("Remuneração base", value=1988.35, disabled=True, label_visibility="collapsed")
    sub_ref = st.number_input("Subsídio Refeição (€)", value=0.00, step=1.0, format="%.2f", key="sub_ref")
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

with col_desconta:
    st.markdown("### Desconta (€)")
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
    irs_val = st.number_input("Retenção IRS (€)", value=0.00, step=0.1, format="%.2f", key="irs_val")
    ss_val = st.number_input("Segurança Social (€)", value=0.00, step=0.1, format="%.2f", key="ss_val")
    adse_val = st.number_input("ADSE (€)", value=0.00, step=0.1, format="%.2f", key="adse_val")

st.markdown("---")

if st.button("Validar e Emitir Recibo Final 🚀", use_container_width=True):
    erros = []
    if abs(sub_ref - 104.00) > 0.1:
        erros.append("❌ **Subsídio de Refeição:** Revê o produto dos 20 dias pelos 5,20 €.")
    if abs(irs_val - 405.62) > 0.1:
        erros.append("❌ **Retenção de IRS:** Aplica os 20,4% sobre os 1 988,35 €.")
    if abs(ss_val - 218.72) > 0.1:
        erros.append("❌ **Segurança Social:** Aplica os 11% sobre os 1 988,35 €.")
    if abs(adse_val - 69.59) > 0.1:
        erros.append("❌ **ADSE:** Aplica os 3,5% sobre os 1 988,35 €.")

    if not erros:
        total_descontos = irs_val + ss_val + adse_val
        salario_liquido = rem_base - total_descontos
        valor_final = salario_liquido + sub_ref

        st.success("🎯 **Excelente trabalho! Todos os cálculos estão corretos.**")
        
        tabela_final = {
            "Rubrica": [
                "Remuneração base", 
                "Subsídio de refeição", 
                "Retenção na fonte (IRS)", 
                "Contribuição para a SS", 
                "Contribuição para a ADSE",
                "---",
                "Salário líquido",
                "Valor recebido no final do mês"
            ],
            "Recebe (€)": [
                f"{rem_base:.2f}", f"{sub_ref:.2f}", "-", "-", "-", "---",
                f"{salario_liquido:.2f}", f"{valor_final:.2f}"
            ],
            "Desconta (€)": [
                "-", "-", f"{irs_val:.2f}", f"{ss_val:.2f}", f"{adse_val:.2f}", "---",
                "-", "-"
            ]
        }
        st.table(pd.DataFrame(tabela_final))
    else:
        for err in erros:
            st.error(err)
