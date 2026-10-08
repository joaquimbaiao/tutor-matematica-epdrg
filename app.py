import os
import csv
from datetime import datetime
import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Tarefa 4 - Modelos Matemáticos para a cidadania",
    page_icon="📐",
    layout="wide"
)

# --- 2. CONFIGURAÇÃO DO MODELO GEMINI (ANTI-404 COM FALLBACK) ---
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
    st.error("Chave de API não configurada. Configura 'GEMINI_API_KEY' nos Secrets do Streamlit.")
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

# --- 3. GESTÃO DO FICHEIRO CSV DE MONITORIZAÇÃO ---
CSV_FILE = "monitorizacao_tarefa4.csv"

def registar_interacao_csv(turma, aluno, exercicio, feedback):
    campos = ["data_hora", "turma", "nome_aluno", "exercicio", "feedback_resumido"]
    ficheiro_existe = os.path.isfile(CSV_FILE)
    resumo = feedback.replace("\n", " ").strip()[:300]
    
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        if not ficheiro_existe:
            writer.writeheader()
        writer.writerow({
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "turma": turma,
            "nome_aluno": aluno,
            "exercicio": exercicio,
            "feedback_resumido": resumo
        })

# --- 4. BASE DE DADOS DOS EXERCÍCIOS ---
exercicios_dados = {
    "Exemplo Guiado: Vencimento Mensal com ADSE": {
        "enunciado": """
O funcionário aufere uma **Remuneração Base de 1 988,35 €**.
Trabalhou 20 dias úteis com subsídio de alimentação de **5,20 €/dia**.
Está sujeito a:
* **11%** para a Segurança Social;
* **20,4%** de retenção na fonte de IRS;
* **3,5%** de contribuição para a ADSE.
""",
        "prompt_contexto": "O aluno deve calcular a remuneração ilíquida, os descontos exatos para Segurança Social (11%), IRS (20,4%) e ADSE (3,5%) e subtrair para obter o salário líquido."
    },
    "Exercício 1: O Caso do Mateus (Açores - Setembro de 2022)": {
        "enunciado": """
O Mateus reside e trabalha na Região Autónoma dos Açores.
Analisa a remuneração base, subsídios aplicáveis e as taxas específicas da região para apurar o valor líquido recebido em setembro de 2022.
""",
        "prompt_contexto": "Verifica se o aluno aplicou corretamente as retenções e deduções específicas para a Região Autónoma dos Açores."
    },
    "Exercício 2.1: Carlos na Madeira (Fevereiro de 2010)": {
        "enunciado": """
O Carlos exerce funções na Região Autónoma da Madeira.
Calcula o vencimento líquido considerando os dias úteis do mês de fevereiro de 2010 e a tabela de retenção em vigor à data.
""",
        "prompt_contexto": "Verifica o apuramento dos dias de subsídio de alimentação e as respetivas taxas de incidência."
    },
    "Exercício 2.2: Carlos em Lisboa (Fevereiro de 2023)": {
        "enunciado": """
O Carlos foi transferido para Lisboa em fevereiro de 2023.
Determina o impacto da mudança no seu salário líquido, tendo em conta as novas tabelas de retenção do Continente.
""",
        "prompt_contexto": "Compara as diferenças de retenção entre a Madeira e o Continente e valida o resultado final."
    },
    "Exercício 3: Mariana na Junta de Freguesia (Exame MACS 2023)": {
        "enunciado": """
A Mariana trabalha numa Junta de Freguesia.
Aplica as regras de cálculo salarial, subsídios adicionais e deduções obrigatórias constantes no problema de exame.
""",
        "prompt_contexto": "Aplica o rigor dos critérios do exame de MACS 2023 quanto à precisão e etapas de cálculo."
    },
    "Exercício 4: Catarina após a Maternidade (Setembro de 2023)": {
        "enunciado": """
A Catarina regressou ao trabalho após licença parental em setembro de 2023.
Calcula o vencimento proporcional aos dias trabalhados e as respetivas deduções fiscais e contributivas.
""",
        "prompt_contexto": "Confere o cálculo proporcional dos dias trabalhados e se as taxas incidem sobre a remuneração proporcional exata."
    },
    "Exercício 5: Carina no Porto (Tabela com Fórmula de Abate)": {
        "enunciado": """
A Carina trabalha no Porto e o seu IRS é determinado através das novas tabelas com taxa marginal e **parcela a abater**.
Determina a retenção efetiva de IRS e o vencimento líquido final.
""",
        "prompt_contexto": "Verifica minuciosamente se o aluno aplicou a fórmula de abate: (Remuneração x Taxa Marginal) - Parcela a Abater."
    }
}

# --- 5. BARRA LATERAL (LAYOUT FIEL À IMAGEM) ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    
    st.markdown("## **EPDR Grândola**")
    st.markdown("##### **Tarefa 4 - Modelos Matemáticos para a cidadania**")
    
    st.markdown("**Nome do Aluno:**")
    nome_aluno = st.text_input("Nome do Aluno", placeholder="Escreve o teu nome completo", label_visibility="collapsed")
    
    st.markdown("**Turma:**")
    turma = st.selectbox(
        "Turma",
        ["10º TCP/TRB", "10º A", "10º B", "11º TCP/TRB", "11º A", "12º TCP/TRB", "12º A"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📍 Lista de Exercícios")
    
    opcoes_exercicios = list(exercicios_dados.keys())
    
    # Ícones estilizados como no ecrã
    opcoes_formatadas = [
        f"👉 {opcoes_exercicios[0]}"
    ] + [f"⚪ {nome}" for nome in opcoes_exercicios[1:]]
    
    escolha_formatada = st.radio(
        "Exercícios",
        opcoes_formatadas,
        label_visibility="collapsed"
    )
    
    # Recupera o nome exato da chave
    indice_escolhido = opcoes_formatadas.index(escolha_formatada)
    exercicio_atual = opcoes_exercicios[indice_escolhido]
    
    st.markdown("---")
    # Monitorização do Professor: Download do CSV
    if os.path.isfile(CSV_FILE):
        with open(CSV_FILE, "rb") as f:
            st.download_button(
                label="📥 Descarregar Folha de Monitorização (CSV)",
                data=f,
                file_name=f"monitorizacao_alunos_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

# --- 6. ÁREA PRINCIPAL: ENUNCIADO E SUBMISSÃO ---
dados_ex = exercicios_dados[exercicio_atual]

# Apresentação do enunciado
st.markdown(dados_ex["enunciado"])

st.markdown("## 📸 Passo 1: Faz os cálculos no caderno e tira uma fotografia")
st.caption("Usa o caderno para estruturar o raciocínio. O Tutor lê as tuas contas e diz-te se estás no bom caminho.")

# Duas colunas exatamente como na captura
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

# Escolhe a foto disponível
imagem_final = foto_cam if foto_cam is not None else foto_upload

# --- 7. PRÉ-VISUALIZAÇÃO E ANÁLISE ---
if imagem_final is not None:
    img = Image.open(imagem_final)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.image(img, caption="A tua folha de cálculos", use_container_width=True)
    
    if st.button("🔍 Pedir Análise ao Tutor IA", type="primary", use_container_width=True):
        if not nome_aluno.strip():
            st.warning("⚠️ Por favor, escreve o teu nome completo na barra lateral antes de pedir a análise.")
        else:
            with st.spinner("A analisar a tua folha de cálculos..."):
                try:
                    model = obter_modelo()
                    prompt = (
                        f"És um tutor pedagógico da disciplina de Modelos Matemáticos para a Cidadania / MACS na EPDR Grândola. "
                        f"Aluno: {nome_aluno} (Turma: {turma}).\n"
                        f"Exercício: {exercicio_atual}.\n"
                        f"Enunciado e Dados: {dados_ex['enunciado']}\n"
                        f"Foco didático: {dados_ex['prompt_contexto']}\n\n"
                        "Analisa a folha de cálculos manuscrita do aluno na imagem com o máximo rigor:\n"
                        "1. Confere todos os passos e operações aritméticas (taxas, multiplicações e subtrações finais).\n"
                        "2. Se existir algum erro, identifica com precisão a linha/etapa onde ocorreu e explica a razão do engano, dando pistas para o aluno corrigir sem apenas entregar a resposta final.\n"
                        "3. Se estiver tudo correto, elogia o rigor matemático e confirma o valor final obtido.\n"
                        "4. Responde de forma clara, motivadora e estruturada em português de Portugal."
                    )
                    
                    response = model.generate_content([prompt, img])
                    feedback_ia = response.text
                    
                    st.success("Análise concluída com sucesso!")
                    st.markdown(feedback_ia)
                    
                    # Guarda os dados na folha CSV
                    registar_interacao_csv(turma, nome_aluno, exercicio_atual, feedback_ia)
                    st.caption("✅ Resolução e feedback registados na monitorização da turma.")
                    
                except Exception as e:
                    st.error(f"Erro ao processar imagem com a IA: {e}")
