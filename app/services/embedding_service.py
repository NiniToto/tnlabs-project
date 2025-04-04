from langchain_huggingface import HuggingFaceEmbeddings
from ..core.config import settings

class EmbeddingService:
    """임베딩 모델 서비스"""
    
    def __init__(self, model_name=None):
        """임베딩 모델 초기화"""
        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME
        self.embeddings = self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """HuggingFace 임베딩 모델 초기화"""
        return HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    
    def get_embeddings(self):
        """임베딩 모델 반환"""
        return self.embeddings

# 싱글톤 인스턴스 생성
embedding_service = EmbeddingService() 