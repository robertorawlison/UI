import streamlit as st
import os
from api_client import api_client

# Configuração da página
st.set_page_config(
    page_title="FADEX Medical Document Analysis",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para replicar o design da imagem
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #8B5CF6 0%, #7C3AED 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    .step-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-left: 4px solid #8B5CF6;
    }
    
    .step-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .step-number {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 18px;
        margin-right: 1rem;
        color: white;
    }
    
    .step-number.active {
        background-color: #8B5CF6;
    }
    
    .step-number.inactive {
        background-color: #E5E7EB;
        color: #6B7280;
    }
    
    .step-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1F2937;
        margin: 0;
    }
    
    .success-message {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #A7F3D0;
        margin: 1rem 0;
    }
    
    .error-message {
        background-color: #FEE2E2;
        color: #DC2626;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #FECACA;
        margin: 1rem 0;
    }
    
    .upload-area {
        border: 2px dashed #D1D5DB;
        border-radius: 10px;
        padding: 3rem;
        text-align: center;
        background-color: #FAFAFA;
        margin: 1rem 0;
    }
    
    .upload-area:hover {
        border-color: #8B5CF6;
        background-color: #F8FAFC;
    }
    
    .results-container {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-top: 1rem;
    }
    
    .category-group {
        background: white;
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
    }
    
    .category-title {
        color: #8B5CF6;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>FADEX Medical Document Analysis</h1>
        <p>A UI to interact with the FADEX API.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar session state
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    if "edital_id" not in st.session_state:
        st.session_state.edital_id = None
    
    # Etapa 1: Geração de Token
    st.markdown("""
    <div class="step-container">
        <div class="step-header">
            <div class="step-number active">1</div>
            <h3 class="step-title">Generate Access Token</h3>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("token_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            client_id = st.text_input("Client ID", value="test_client", help="Enter your client ID")
        
        with col2:
            client_secret = st.text_input("Client Secret", type="password", help="Enter your client secret")
        
        submit_token = st.form_submit_button("Generate Token", type="primary")
        
        if submit_token:
            if client_id and client_secret:
                with st.spinner("Generating token..."):
                    result = api_client.generate_token(client_id, client_secret)
                    
                if result and "access_token" in result:
                    st.session_state.access_token = result["access_token"]
                    st.markdown("""
                    <div class="success-message">
                        ✅ Token gerado com sucesso! Você pode prosseguir para a próxima etapa.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="error-message">
                        ❌ Erro ao gerar token. Verifique suas credenciais.
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Por favor, preencha todos os campos.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Etapa 2: Upload de Edital
    has_token = st.session_state.access_token is not None
    
    st.markdown(f"""
    <div class="step-container">
        <div class="step-header">
            <div class="step-number {'active' if has_token else 'inactive'}">2</div>
            <h3 class="step-title">Upload Edital (PDF)</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if has_token:
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="edital_upload")
        
        if uploaded_file is not None:
            if st.button("Upload Edital", type="primary"):
                with st.spinner("Uploading edital..."):
                    result = api_client.upload_edital(uploaded_file)
                
                if result and "edital_id" in result:
                    st.session_state.edital_id = result["edital_id"]
                    st.markdown(f"""
                    <div class="success-message">
                        ✅ Edital carregado com sucesso!<br>
                        <strong>Edital ID:</strong> {result["edital_id"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="error-message">
                        ❌ Erro ao fazer upload do edital.
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("🔒 Faça login primeiro para acessar esta funcionalidade.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Etapa 3: Categorização de Exames
    has_edital = st.session_state.edital_id is not None
    
    st.markdown(f"""
    <div class="step-container">
        <div class="step-header">
            <div class="step-number {'active' if has_edital else 'inactive'}">3</div>
            <h3 class="step-title">Categorize Medical Exams</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if has_edital:
        uploaded_files = st.file_uploader(
            "Choose exam files", 
            type=["png", "jpg", "jpeg", "pdf"], 
            accept_multiple_files=True,
            key="exams_upload"
        )
        
        if uploaded_files:
            st.info(f"📁 {len(uploaded_files)} arquivo(s) selecionado(s)")
            
            if st.button("Categorize Exams", type="primary"):
                with st.spinner("Categorizing exams..."):
                    result = api_client.categorize_exams(uploaded_files, st.session_state.edital_id)
                
                if result:
                    display_categorization_results(result)
                else:
                    st.markdown("""
                    <div class="error-message">
                        ❌ Erro ao categorizar exames.
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("🔒 Faça upload do edital primeiro para acessar esta funcionalidade.")
    
    st.markdown("</div>", unsafe_allow_html=True)

def display_categorization_results(result):
    """Display categorization results in a formatted way"""
    st.markdown("""
    <div class="results-container">
        <h3>📊 Resultados da Categorização</h3>
    """, unsafe_allow_html=True)
    
    # Resumo dos resultados
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Exames Enviados", len(result.get("exames_enviados", [])))
    
    with col2:
        st.metric("Status Comparação", result.get("comparacao", {}).get("status", "N/A"))
    
    with col3:
        st.metric("Situação Incapacitante", result.get("situacao_incapacitante", {}).get("status", "N/A"))
    
    # Exames enviados
    if result.get("exames_enviados"):
        st.subheader("📋 Exames Enviados")
        for exame in result["exames_enviados"]:
            st.write(f"• {exame}")
    
    # Resultados da categorização
    if result.get("categorization_results"):
        st.subheader("🏷️ Categorias Encontradas")
        
        for categoria, itens in result["categorization_results"].items():
            st.markdown(f"""
            <div class="category-group">
                <div class="category-title">{categoria}</div>
            """, unsafe_allow_html=True)
            
            for item in itens:
                nome_exame = item.get("nome_exame", [])
                if isinstance(nome_exame, list):
                    nome_exame = ", ".join(nome_exame)
                st.write(f"**{item.get('name', 'N/A')}**: {nome_exame}")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Comparação com exames obrigatórios
    if result.get("comparacao"):
        st.subheader("⚖️ Comparação com Exames Obrigatórios")
        comparacao = result["comparacao"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Exames Faltando:**")
            for exame in comparacao.get("exames_faltando", []):
                st.write(f"• ❌ {exame}")
        
        with col2:
            st.write("**Exames Extras:**")
            for exame in comparacao.get("exames_extras", []):
                st.write(f"• ➕ {exame}")
    
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
