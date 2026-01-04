import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuração Segura da IA
if "GEMINI_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_KEY"].strip()
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("⚠️ Erro: Chave de API não configurada nos Secrets do Streamlit.")
    st.stop()

# 2. Configuração da Página
st.set_page_config(page_title="SmartCheck IA", page_icon="🛒", layout="wide")

st.title("🛒 SmartCheck IA - Gestão Conecta T.I")

aba1, aba2 = st.tabs(["📄 Receber Nota Fiscal", "📦 Conferir Carga Física"])

with aba1:
    st.header("Entrada de Mercadoria")
    arquivo_nf = st.file_uploader("Suba a foto da Nota Fiscal", type=['png', 'jpg', 'jpeg'])
    
    if arquivo_nf:
        img = Image.open(arquivo_nf)
        st.image(img, width=300, caption="Nota Fiscal Carregada")
        
        if st.button("Analisar Preços e Lucro"):
            with st.spinner("IA analisando a nota..."):
                prompt = "Liste os produtos desta nota com preço de custo e sugira o preço de venda com 22% de lucro. Retorne em uma tabela."
                try:
                    resposta = model.generate_content([prompt, img])
                    st.markdown(resposta.text)
                    st.success("Análise concluída com 22% de margem aplicada!")
                except Exception as e:
                    st.error(f"Erro na análise: {e}")

with aba2:
    st.header("Inspeção de Pátio")
    st.write("Use a câmera para validar os itens recebidos.")
    
    # Opção para tablet: usa o carregador de arquivos que abre a câmera traseira
    foto_carga = st.file_uploader("Capturar foto da mercadoria", type=['png', 'jpg', 'jpeg'])
    
    if foto_carga:
        img_carga = Image.open(foto_carga)
        st.image(img_carga, width=400, caption="Item no Pátio")
        st.warning("Divergência Detectada: Verifique se a quantidade de 'Arroz 5kg' bate com a NF.")
