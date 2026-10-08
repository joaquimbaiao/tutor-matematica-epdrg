import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Tutor IA - Folha de Vencimento", layout="centered")

st.title("Tutor IA")
st.caption("Análise de folha de cálculos e vencimentos")

# --- OBTENÇÃO DA API KEY ---
# Tenta obter pelo secrets do Streamlit Cloud ou variável de ambiente
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

# Configuração da API do Google Gemini
genai.configure(api_key=api_key)

# --- FUNÇÃO DE SELEÇÃO DO MODELO COM FALLBACK AUTOMÁTICO ---
@st.cache_resource
def obter_modelo():
    """Garante a escolha de um modelo válido para generateContent sem dar 404."""
    # Lista de prioridade com nomes padrão
    preferenciais = [
        "gemini-1.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-pro",
        "gemini-flash-latest",
    ]
    
    try:
        # Consulta os modelos que a tua chave tem permissão para aceder
        disponiveis = [
            m.name.replace("models/", "") 
            for m in genai.list_models() 
            if "generateContent" in m.supported_generation_methods
        ]
        
        # Escolhe o primeiro da lista preferencial que estiver disponível
        for pref in preferenciais:
            if pref in disponiveis:
                return genai.GenerativeModel(pref)
        
        # Se nenhum preferencial for encontrado, usa o primeiro disponível
        if disponiveis:
            return genai.GenerativeModel(disponiveis[0])
            
    except Exception:
        # Se list_models falhar por rede ou versão, recorre à string padrão
        pass

    return genai.GenerativeModel("gemini-1.5-flash")

# --- INTERFACE: CAPTURA OU UPLOAD DA FOLHA ---
st.subheader("A tua folha de cálculos")
imagem_capturada = st.camera_input("Tira uma foto da folha")

# Fallback opcional: upload de ficheiro caso a câmara não abra
if not imagem_capturada:
    imagem_capturada = st.file_uploader("Ou faz upload de uma imagem", type=["png", "jpg", "jpeg"])

# --- PROCESSAMENTO COM O TUTOR IA ---
if imagem_capturada is not None:
    # Carregar imagem com PIL
    img = Image.open(imagem_capturada)

    if st.button("🔍 Pedir Análise ao Tutor IA", type="primary"):
        with st.spinner("A analisar a tua folha de cálculos..."):
            try:
                model = obter_modelo()
                
                prompt = (
                    "És um tutor especializado em cálculos financeiros e folhas de vencimento. "
                    "Analisa os cálculos apresentados nesta imagem com rigor. "
                    "Verifica se há erros de cálculo, passos omissos ou fórmulas incorretas. "
                    "Apresenta a resposta de forma didática, direta e clara."
                )
                
                # Chamada multimodal (texto + imagem)
                response = model.generate_content([prompt, img])
                
                st.success("Análise concluída!")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Erro ao processar imagem com a IA: {e}")
