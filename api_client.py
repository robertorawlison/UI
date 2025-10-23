import requests
import streamlit as st
from typing import Dict, Any, List, Optional
from config import API_BASE_URL

class FadexAPIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authorization token if available"""
        headers = {"Content-Type": "application/json"}
        if "access_token" in st.session_state:
            headers["Authorization"] = f"Bearer {st.session_state.access_token}"
        return headers
    
    def generate_token(self, client_id: str, client_secret: str) -> Dict[str, Any]:
        """Generate access token"""
        url = f"{self.base_url}/generate-token/"
        data = {
            "client_id": client_id,
            "client_secret": client_secret
        }
        
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao gerar token: {str(e)}")
            return {}
    
    def upload_edital(self, file) -> Dict[str, Any]:
        """Upload edital PDF"""
        url = f"{self.base_url}/edital/upload"
        
        try:
            files = {"file": (file.name, file, "application/pdf")}
            headers = {}
            if "access_token" in st.session_state:
                headers["Authorization"] = f"Bearer {st.session_state.access_token}"
            
            response = self.session.post(url, files=files, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao fazer upload do edital: {str(e)}")
            return {}
    
    def categorize_exams(self, files: List, edital_id: str) -> Dict[str, Any]:
        """Categorize medical exams"""
        url = f"{self.base_url}/categorizar-com-edital/"
        
        try:
            files_data = []
            for file in files:
                files_data.append(("files", (file.name, file, file.type)))
            
            data = {"edital_id": edital_id}
            headers = {}
            if "access_token" in st.session_state:
                headers["Authorization"] = f"Bearer {st.session_state.access_token}"
            
            response = self.session.post(url, files=files_data, data=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao categorizar exames: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    st.error(f"Detalhes do erro: {error_detail}")
                except:
                    st.error(f"Resposta do servidor: {e.response.text}")
            return {}

# Global API client instance
api_client = FadexAPIClient()
