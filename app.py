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
        margin-bottom: 2rem;
        border-left: 4px solid #8B5CF6;
        padding-left: 1rem;
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
        color: #000000 !important;
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
        margin-top: 1rem;
    }
    
    .category-group {
        background: #F8FAFC;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .category-title {
        color: #000000 !important;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Remover links e deixar texto branco */
    a {
        color: white !important;
        text-decoration: none !important;
    }
    
    a:hover {
        color: white !important;
        text-decoration: none !important;
    }
    
    /* Garantir que todos os textos sejam brancos */
    .stMarkdown, .stText, .stWrite, .stSelectbox, .stTextInput, .stTextArea {
        color: white !important;
    }
    
    /* Remover links de todos os elementos Streamlit */
    .stMarkdown a, .stText a, .stWrite a {
        color: white !important;
        text-decoration: none !important;
    }
    
    /* Fundo escuro para o texto branco */
    .main .block-container {
        background-color: #1a1a1a;
        color: white;
    }
    
    /* Garantir que todos os elementos tenham fundo escuro */
    .stApp {
        background-color: #1a1a1a;
    }
    
    .stApp > div {
        background-color: #1a1a1a;
    }
    
    /* Forçar cor branca em todos os textos */
    * {
        color: white !important;
    }
    
    /* Exceções para elementos que precisam manter suas cores */
    .metric-card {
        color: white !important;
    }
    
    .step-number {
        color: white !important;
    }
    
    /* Remover todos os links do Streamlit */
    .stApp a, .stApp a:visited, .stApp a:hover, .stApp a:active {
        color: white !important;
        text-decoration: none !important;
    }
    
    /* Garantir que labels e textos sejam brancos */
    .stLabel, .stText, .stMarkdown, .stWrite, .stSelectbox label, .stTextInput label {
        color: white !important;
    }
    
    /* Remover links de elementos específicos */
    .stMarkdown a, .stText a, .stWrite a, .stSelectbox a, .stTextInput a {
        color: white !important;
        text-decoration: none !important;
    }
    
    /* Mensagens de sucesso com texto preto */
    .stSuccess, .stSuccess * {
        color: #000000 !important;
    }
    
    /* Mensagens de info com texto preto */
    .stInfo, .stInfo * {
        color: #000000 !important;
    }
    
    /* Textos dos exames em preto */
    .exam-item, .exam-item * {
        color: #000000 !important;
    }
    
    .exam-detail, .exam-detail * {
        color: #000000 !important;
    }
    
    .comparison-item, .comparison-item * {
        color: #000000 !important;
    }
    
    .category-item, .category-item * {
        color: #000000 !important;
    }
    
    /* Forçar texto preto em divs específicos dos exames */
    div[style*="background: #F8FAFC"], 
    div[style*="background: white"], 
    div[style*="background: #F0FDF4"], 
    div[style*="background: #FEF2F2"] {
        color: #000000 !important;
    }
    
    div[style*="background: #F8FAFC"] *, 
    div[style*="background: white"] *, 
    div[style*="background: #F0FDF4"] *, 
    div[style*="background: #FEF2F2"] * {
        color: #000000 !important;
    }
    
    /* Títulos das etapas em branco */
    .step-title {
        color: white !important;
    }
    
    /* Títulos dos resultados em preto */
    .results-container h3,
    .results-container h4,
    .results-container h5,
    .results-container h6 {
        color: #000000 !important;
    }
    
    /* Títulos dentro de divs com fundo */
    div[style*="background"] h3,
    div[style*="background"] h4,
    div[style*="background"] h5,
    div[style*="background"] h6 {
        color: #000000 !important;
    }
    
    /* Forçar texto preto em seções específicas de resultado */
    .result-section, .result-section * {
        color: #000000 !important;
    }
    
    /* Forçar texto preto em divs com fundo específico */
    div[style*="background: #FEF2F2"] *,
    div[style*="background: #D1FAE5"] *,
    div[style*="background: #F8FAFC"] * {
        color: #000000 !important;
    }
    
    /* Forçar texto preto em todos os elementos dentro de divs de resultado */
    div[style*="border-left: 4px solid #EF4444"] *,
    div[style*="border-left: 4px solid #22C55E"] *,
    div[style*="border-left: 4px solid #8B5CF6"] * {
        color: #000000 !important;
    }
    
    /* Regra mais específica para forçar texto preto */
    .stApp .result-section,
    .stApp .result-section *,
    .stApp .result-section h4,
    .stApp .result-section p,
    .stApp .result-section strong,
    .stApp .result-section span {
        color: #000000 !important;
    }
    
    /* Sobrescrever qualquer CSS do Streamlit */
    div[class*="result-section"] * {
        color: #000000 !important;
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
    if "categorization_result" not in st.session_state:
        st.session_state.categorization_result = None
    
    # Sidebar com controles
    with st.sidebar:
        st.header("🔧 Controles")
        
        if st.button("🔄 Reset All", type="secondary", help="Limpar todos os dados e começar novamente"):
            # Limpar todos os dados da sessão
            for key in ["access_token", "edital_id", "categorization_result"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        st.subheader("📊 Status")
        st.write(f"🔐 Token: {'✅ Ativo' if st.session_state.access_token else '❌ Não gerado'}")
        st.write(f"📄 Edital: {'✅ Carregado' if st.session_state.edital_id else '❌ Não carregado'}")
        st.write(f"🏥 Resultados: {'✅ Disponíveis' if st.session_state.categorization_result else '❌ Não disponíveis'}")
    
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
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("Categorize Exams", type="primary"):
                    with st.spinner("Categorizing exams..."):
                        result = api_client.categorize_exams(uploaded_files, st.session_state.edital_id)
                    
                    if result:
                        st.session_state.categorization_result = result
                        st.success("✅ Exames categorizados com sucesso!")
                    else:
                        st.markdown("""
                        <div class="error-message">
                            ❌ Erro ao categorizar exames.
                        </div>
                        """, unsafe_allow_html=True)
            
            with col2:
                if st.button("🔄 Reset Results", help="Limpar resultados e permitir novos uploads"):
                    if "categorization_result" in st.session_state:
                        del st.session_state.categorization_result
                    st.success("🔄 Resultados limpos com sucesso!")
        
        # Mostrar resultados se existirem (apenas uma vez)
        if "categorization_result" in st.session_state:
            st.markdown("---")
            display_categorization_results(st.session_state.categorization_result)
    else:
        st.info("🔒 Faça upload do edital primeiro para acessar esta funcionalidade.")
    
    st.markdown("</div>", unsafe_allow_html=True)

def display_categorization_results(result):
    """Display categorization results in a formatted way"""
    st.markdown("""
    <h3 style="color: #000000 !important;">📊 Resultados da Categorização</h3>
    """, unsafe_allow_html=True)
    
    # Verificar se result é um dicionário
    if not isinstance(result, dict) or result is None:
        return
    
    # Resumo dos resultados com cards estilizados
    col1, col2, col3 = st.columns(3)
    
    with col1:
        exames_enviados = result.get("exames_enviados", [])
        count = len(exames_enviados) if isinstance(exames_enviados, list) else 0
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{count}</p>
            <p class="metric-label">Exames Enviados</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        comparacao = result.get("comparacao", {})
        status_comparacao = comparacao.get("status", "N/A") if isinstance(comparacao, dict) else "N/A"
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{status_comparacao}</p>
            <p class="metric-label">Status Comparação</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        situacao = result.get("situacao_incapacitante", {})
        status_situacao = situacao.get("status", "N/A") if isinstance(situacao, dict) else "N/A"
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{status_situacao}</p>
            <p class="metric-label">Situação Incapacitante</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Exames enviados com melhor formatação
    exames_enviados = result.get("exames_enviados", [])
    if exames_enviados and isinstance(exames_enviados, list):
        st.markdown("""
        <h3 style="color: #000000 !important;">📋 Exames Enviados</h3>
        """, unsafe_allow_html=True)
        
        # Criar colunas para exibir exames em grid
        cols = st.columns(3)
        for i, exame in enumerate(exames_enviados):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="exam-item" style="background: #F8FAFC; padding: 0.5rem; border-radius: 6px; border-left: 3px solid #8B5CF6; margin: 0.25rem 0; color: #000000 !important;">
                    📄 {exame}
                </div>
                """, unsafe_allow_html=True)
    
    # Resultados da categorização com melhor layout
    categorization_results = result.get("categorization_results", {})
    if categorization_results and isinstance(categorization_results, dict):
        st.markdown("""
        <h3 style="color: #000000 !important;">🏷️ Categorias Encontradas</h3>
        """, unsafe_allow_html=True)
        
        for categoria, itens in categorization_results.items():
            st.markdown(f"""
            <div class="category-group">
                <div class="category-title" style="color: #000000 !important;">📁 {categoria}</div>
            """, unsafe_allow_html=True)
            
            if isinstance(itens, list):
                for item in itens:
                    if isinstance(item, dict):
                        nome_exame = item.get("nome_exame", [])
                        if isinstance(nome_exame, list):
                            nome_exame = ", ".join(nome_exame)
                        st.markdown(f"""
                        <div class="category-item" style="background: white; padding: 0.75rem; border-radius: 4px; margin: 0.25rem 0; border: 1px solid #E5E7EB; color: #000000 !important;">
                            <strong style="color: #000000 !important;">📄 {item.get('name', 'N/A')}</strong><br>
                            <span style="color: #000000 !important; font-size: 0.9rem;">{nome_exame}</span>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Comparação com exames obrigatórios
    comparacao = result.get("comparacao", {})
    if comparacao and isinstance(comparacao, dict):
        st.markdown("""
        <h3 style="color: #000000 !important;">⚖️ Comparação com Exames Obrigatórios</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**❌ Exames Faltando:**")
            exames_faltando = comparacao.get("exames_faltando", [])
            if isinstance(exames_faltando, list) and exames_faltando:
                for exame in exames_faltando:
                    st.markdown(f"""
                    <div class="comparison-item" style="background: #FEF2F2; padding: 0.5rem; border-radius: 4px; border-left: 3px solid #EF4444; margin: 0.25rem 0; color: #000000 !important;">
                        ❌ {exame}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("✅ Nenhum exame faltando")
        
        with col2:
            st.markdown("**➕ Exames Extras:**")
            exames_extras = comparacao.get("exames_extras", [])
            if isinstance(exames_extras, list) and exames_extras:
                for exame in exames_extras:
                    st.markdown(f"""
                    <div class="comparison-item" style="background: #F0FDF4; padding: 0.5rem; border-radius: 4px; border-left: 3px solid #10B981; margin: 0.25rem 0; color: #000000 !important;">
                        ➕ {exame}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("✅ Nenhum exame extra")
    
    # Situação de incapacitante
    situacao_incapacitante = result.get("situacao_incapacitante", {})
    if situacao_incapacitante and isinstance(situacao_incapacitante, dict):
        st.markdown("""
        <h3 style="color: #000000 !important;">🚨 Situação de Incapacitante</h3>
        """, unsafe_allow_html=True)
        
        # Inicializar variáveis
        resultado = "N/A"
        motivo = "N/A"
        situacao_geral = "N/A"
        tem_incapacitante = False
        
        # Navegar pela estrutura aninhada para encontrar incapacitante e motivo
        for categoria, dados in situacao_incapacitante.items():
            if isinstance(dados, dict):
                # Extrair situação geral se disponível
                if "situacao_geral" in dados:
                    situacao_geral = dados["situacao_geral"]
                
                # Procurar nos detalhes por incapacitante e motivo
                if "detalhes" in dados and isinstance(dados["detalhes"], list):
                    for detalhe in dados["detalhes"]:
                        if isinstance(detalhe, dict):
                            if "incapacitante" in detalhe:
                                resultado = detalhe["incapacitante"]
                                tem_incapacitante = resultado == "Sim"
                            if "motivo" in detalhe:
                                motivo = detalhe["motivo"]
        
        # Exibir situação geral se disponível
        if situacao_geral != "N/A":
            st.markdown(f"""
            <div class="result-section" style="background: #F8FAFC; padding: 1rem; border-radius: 8px; border-left: 4px solid #8B5CF6; margin: 1rem 0; color: #000000 !important;">
                <h4 style="color: #000000 !important; margin: 0 0 0.5rem 0; font-weight: bold;">📋 Situação Geral</h4>
                <p style="color: #000000 !important; margin: 0; font-weight: bold;">{situacao_geral}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if tem_incapacitante:
            st.markdown(f"""
            <div class="result-section" style="background: #FEF2F2; padding: 1rem; border-radius: 8px; border-left: 4px solid #EF4444; margin: 1rem 0; color: #000000 !important;">
                <h4 style="color: #000000 !important; margin: 0 0 0.5rem 0; font-weight: bold;">⚠️ INCAPACITANTE DETECTADO</h4>
                <p style="color: #000000 !important; margin: 0; font-weight: bold;"><strong style="color: #000000 !important;">Resultado:</strong> <span style="color: #000000 !important;">{resultado}</span></p>
                <p style="color: #000000 !important; margin: 0; font-weight: bold;"><strong style="color: #000000 !important;">Motivo:</strong> <span style="color: #000000 !important;">{motivo}</span></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-section" style="background: #D1FAE5; padding: 1rem; border-radius: 8px; border-left: 4px solid #22C55E; margin: 1rem 0; color: #000000 !important;">
                <h4 style="color: #000000 !important; margin: 0 0 0.5rem 0; font-weight: bold;">✅ NENHUM INCAPACITANTE DETECTADO</h4>
                <p style="color: #000000 !important; margin: 0; font-weight: bold;"><strong style="color: #000000 !important;">Resultado:</strong> <span style="color: #000000 !important;">{resultado}</span></p>
                <p style="color: #000000 !important; margin: 0; font-weight: bold;"><strong style="color: #000000 !important;">Motivo:</strong> <span style="color: #000000 !important;">{motivo}</span></p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
