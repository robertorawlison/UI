# FADEX Medical Document Analysis - Streamlit UI

Interface Streamlit para interagir com a API FADEX de análise de documentos médicos.

## Funcionalidades

- **🔐 Geração de Token**: Autenticação com client_id e client_secret
- **📄 Upload de Edital**: Upload de arquivos PDF de edital
- **🏥 Categorização de Exames**: Upload e categorização de exames médicos

## Instalação e Execução

1. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

2. **Configurar URL da API:**
Crie um arquivo `.env` na raiz do projeto:
```
API_BASE_URL=http://localhost:8000/fadex
```

3. **Executar a aplicação:**
```bash
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`

## Rotas da API Integradas

- `POST /generate-token/` - Geração de token de acesso
- `POST /edital/upload` - Upload de edital PDF  
- `POST /categorizar-com-edital/` - Categorização de exames

## Estrutura do Projeto

```
├── app.py                 # Aplicação principal Streamlit
├── api_client.py          # Cliente para integração com API
├── config.py              # Configurações
├── requirements.txt       # Dependências Python
└── README.md             # Documentação
```

## Design

A interface replica o design da imagem original com:
- Layout em etapas sequenciais numeradas
- Design moderno com cores roxas (#8B5CF6)
- Áreas de upload com drag & drop
- Exibição de resultados formatados
- Interface responsiva e intuitiva

## Fluxo de Uso

1. **Etapa 1**: Gere um token de acesso com suas credenciais
2. **Etapa 2**: Faça upload de um PDF do edital
3. **Etapa 3**: Faça upload dos exames médicos para categorização
4. **Resultados**: Visualize os resultados da categorização e comparação
