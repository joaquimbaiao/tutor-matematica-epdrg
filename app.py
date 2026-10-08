import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Tarefa 4 - Modelos Matemáticos para a cidadania",
    layout="wide"
)

# --- TÍTULO PRINCIPAL ---
st.title("Tarefa 4 - Modelos Matemáticos para a cidadania")
st.caption("Tutor Inteligente de Apoio à Resolução de Exercícios e Análise de Cálculos")

# --- AUTENTICAÇÃO E API KEY ---
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

# --- FUNÇÃO DE SELEÇÃO DINÂMICA DO MODELO (ANTI-404) ---
@st.cache_resource
def obter_modelo():
    preferenciais = [
        "gemini-1.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-pro",
        "gemini-flash-latest",
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

# --- COMPONENTE REUTILIZÁVEL PARA CADA EXERCÍCIO ---
def renderizar_exercicio(nome_ex, descricao, instrucao_tutor):
    st.markdown(f"### {nome_ex}")
    st.info(descricao)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("**Entrada da Resolução:**")
        modo = st.radio(
            f"Como queres submeter a tua folha ({nome_ex})?",
            ["Câmara", "Upload de Ficheiro"],
            key=f"modo_{nome_ex}",
            horizontal=True
        )

        imagem_arquivo = None
        if modo == "Câmara":
            imagem_arquivo = st.camera_input(f"Fotografa os teus cálculos para {nome_ex}", key=f"cam_{nome_ex}")
        else:
            imagem_arquivo = st.file_uploader(f"Envia a imagem ({nome_ex})", type=["png", "jpg", "jpeg"], key=f"up_{nome_ex}")

    with col2:
        st.write("**Validação e Feedback:**")
        if imagem_arquivo is not None:
            img = Image.open(imagem_arquivo)
            st.image(img, caption="Folha submetida", use_container_width=True)

            if st.button(f"🔍 Pedir Análise ao Tutor IA ({nome_ex})", type="primary", key=f"btn_{nome_ex}"):
                with st.spinner("O Tutor IA está a rever os teus passos de cálculo..."):
                    try:
                        model = obter_modelo()
                        prompt = (
                            f"És um tutor pedagógico rigoroso na disciplina de Modelos Matemáticos para a Cidadania / MACS. "
                            f"O aluno está a resolver o seguinte exercício: {nome_ex}.\n"
                            f"Contexto/Objetivo do problema: {descricao}.\n\n"
                            f"Instruções específicas para a correção: {instrucao_tutor}\n\n"
                            "Analisa a imagem com o trabalho manuscrito do aluno:\n"
                            "1. Identifica a coerência das fórmulas utilizadas.\n"
                            "2. Confere a exatidão dos cálculos numéricos passo a passo.\n"
                            "3. Se houver erro, aponta a linha/passo exato onde ocorreu e explica o porquê sem apenas dar a solução final diretamente, incentivando o raciocínio.\n"
                            "4. Se estiver tudo correto, valida a conclusão e fundamenta o acerto com clareza."
                        )
                        response = model.generate_content([prompt, img])
                        st.success("Análise concluída!")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Erro ao processar com a IA: {e}")
        else:
            st.write("Aguarda a submissão de uma imagem para iniciar a análise.")

# --- DEFINIÇÃO DOS EXERCÍCIOS DA TAREFA ---
# Configura aqui os restantes exercícios, descrições e objetivos pedagógicos específicos:
exercicios = [
    {
        "nome": "Exercício 1: Folha de Vencimento e Descontos",
        "descricao": "Cálculo de remuneração bruta, retenção na fonte (IRS), taxa social única (SS) e determinação do salário líquido.",
        "prompt": "Valida se as percentagens de retenção e segurança social foram aplicadas sobre a base de incidência correta e se a subtração final para o salário líquido bate certo."
    },
    {
        "nome": "Exercício 2: Orçamento Familiar e Poupança",
        "descricao": "Análise de receitas, despesas fixas/variáveis e taxa de esforço associada a encargos mensais.",
        "prompt": "Verifica os cálculos das proporções de despesa, a taxa de esforço percentual e as projeções de saldo líquido ou poupança mensal."
    },
    {
        "nome": "Exercício 3: Crédito e Juros (Simulação)",
        "descricao": "Modelagem de regimes de juro, amortização ou custos totais associados a encargos bancários (TAEG/MTIC).",
        "prompt": "Verifica se as fórmulas de juro ou cálculo do custo total de crédito foram corretamente estruturadas e aplicadas nas iterações temporais."
    },
    {
        "nome": "Exercício 4: Indicadores e Modelos de Decisão",
        "descricao": "Aplicação de proporcionalidade, variação percentual ou índice ponderado na tomada de decisões cívicas/financeiras.",
        "prompt": "Valida a correta utilização de médias ponderadas, taxas de crescimento percentuais e a interpretação matemática do resultado obtido."
    }
]

# --- NAVEGAÇÃO POR ABAS (TABS) ---
abas = st.tabs([ex["nome"] for ex in exercicios])

for i, ex in enumerate(exercicios):
    with abas[i]:
        renderizar_exercicio(
            nome_ex=ex["nome"],
            descricao=ex["descricao"],
            instrucao_tutor=ex["prompt"]
        )
