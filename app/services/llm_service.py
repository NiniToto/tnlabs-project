from langchain_groq import ChatGroq
from app.core.config import GROQ_API_KEY, DEFAULT_LLM_MODEL

class LLMService:
    """LLM 모델 서비스"""
    
    def __init__(self, model_name=None):
        """LLM 모델 초기화"""
        self.model_name = model_name or DEFAULT_LLM_MODEL
        self.llm = self._initialize_llm()
    
    def _initialize_llm(self):
        """Groq LLM 초기화"""
        return ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=self.model_name
        )
    
    def get_llm(self):
        """LLM 모델 반환"""
        return self.llm

# 싱글톤 인스턴스 생성
llm_service = LLMService() 