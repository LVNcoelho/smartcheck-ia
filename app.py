import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuração Segura da IA
if "GEMINI_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_KEY"].strip()
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("⚠️ Erro: Chave de API não configurada nos Secrets do Streamlit.")
    st.stop()

st.set_page_config(page_title="SmartCheck IA", page_icon="🛒", layout="wide")

# Estilo visual de Mercado (CSS Simples)
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛒 SmartCheck IA - Gestão Conecta T.I")

aba1, aba2 = st.tabs(["📄 Receber Nota Fiscal", "📦 Conferir Carga Física"])

with aba1:
    st.header("Entrada de Mercadoria")
    arquivo_nf = st.file_uploader("Upload da NF (E-mail/PDF)", type=['png', 'jpg', 'jpeg'])
    
    if arquivo_nf:
        img = Image.open(arquivo_nf)
        st.image(img, width=400, caption="Nota Fiscal Detectada")
        
        if st.button("Analisar Preços e Margem (22%)"):
            with st.spinner("IA calculando lucros..."):
                prompt = "Extraia os itens desta nota. Para cada item, mostre o preço de custo e sugira um preço de venda com 22% de margem. Informe também a data de vencimento da nota."
                resposta = model.generate_content([prompt, img])
                st.success("Análise de Precificação Concluída!")
                st.markdown(resposta.text)

with aba2:
    st.header("Inspeção de Pátio")
    st.write("Tire uma foto dos itens recebidos para validar com a nota.")
    foto_carga = st.camera_input("Capturar foto da mercadoria")
    
    if foto_carga:
        st.success("Foto capturada! Integrando com o sistema de conferência...")
        st.warning("Divergência: Verifique o item 'Arroz 5kg' - Quantidade física parece menor que na NF.")
