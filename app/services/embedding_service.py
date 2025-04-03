from langchain.embeddings import HuggingFaceEmbeddings
from app.core.config import EMBEDDING_MODEL

class EmbeddingService:
    """임베딩 모델 서비스"""
    
    def __init__(self, model_name=None):
        """임베딩 모델 초기화"""
        self.model_name = model_name or EMBEDDING_MODEL
        self.embeddings = self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """HuggingFace 임베딩 모델 초기화"""
        return HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={'device': 'cpu'}
        )
    
    def get_embeddings(self):
        """임베딩 모델 반환"""
        return self.embeddings

# 싱글톤 인스턴스 생성
embedding_service = EmbeddingService() 