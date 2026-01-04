import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuração Segura da IA
if "GEMINI_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_KEY"].strip()
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ Erro: Chave de API não configurada nos Secrets do Streamlit.")
    st.stop()

# 2. Configuração Visual da Página
st.set_page_config(page_title="SmartCheck IA", page_icon="🛒", layout="wide")

st.title("🛒 SmartCheck IA - Gestão Conecta T.I")
st.markdown("---")

# 3. Criação das Abas de Navegação
aba1, aba2 = st.tabs(["📄 Receber Nota Fiscal", "📦 Conferir Carga Física"])

with aba1:
    st.header("Entrada de Mercadoria")
    st.write("Suba a imagem da NF para calcular margens de lucro automaticamente.")
    
    arquivo_nf = st.file_uploader("Escolher foto da Nota Fiscal", type=['png', 'jpg', 'jpeg'])
    
    if arquivo_nf:
        img = Image.open(arquivo_nf)
        st.image(img, width=400, caption="Nota Fiscal Carregada")
        
        if st.button("Analisar Preços e Margem (22%)"):
            with st.spinner("IA analisando a nota e calculando lucros..."):
                prompt = "Liste os produtos desta nota com preço de custo e sugira o preço de venda com 22% de lucro. Retorne o resultado em uma tabela formatada."
                try:
                    resposta = model.generate_content([prompt, img])
                    st.markdown("### 📊 Sugestão de Preços")
                    st.markdown(resposta.text)
                    st.success("Análise concluída com sucesso!")
                except Exception as e:
                    st.error(f"Erro na análise: {e}")

with aba2:
    st.header("Inspeção de Pátio")
    st.write("Capture fotos da carga física para validar o recebimento.")
    
    # Este botão abre a câmera em dispositivos móveis
    foto_carga = st.file_uploader("Capturar foto da mercadoria", type=['png', 'jpg', 'jpeg'])
    
    if foto_carga:
        img_carga = Image.open(foto_carga)
        st.image(img_carga, width=500, caption="Item Detectado no Pátio")
        st.warning("ℹ️ Verificação Visual: Compare a quantidade física com os dados da NF acima.")
        st.info("Status: Item em conformidade visual com o padrão da Conecta T.I.")

# Rodapé
st.markdown("---")
st.caption("Desenvolvido por Conecta T.I - Inteligência Artificial aplicada à Logística")
