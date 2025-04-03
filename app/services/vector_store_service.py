from langchain_community.vectorstores import FAISS
from app.core.config import VECTOR_STORE_PATH
from app.services.embedding_service import embedding_service
import os

class VectorStoreService:
    """벡터 스토어 서비스"""
    
    def __init__(self, store_path=None):
        """벡터 스토어 초기화"""
        self.store_path = store_path or VECTOR_STORE_PATH
        self.embeddings = embedding_service.get_embeddings()
        self.vector_store = self._load_or_create_vector_store()
    
    def _load_or_create_vector_store(self):
        """벡터 저장소를 로드하거나 새로 생성"""
        os.makedirs(os.path.dirname(self.store_path), exist_ok=True)
        
        if os.path.exists(self.store_path):
            try:
                return FAISS.load_local(self.store_path, self.embeddings)
            except Exception as e:
                print(f"벡터 스토어 로드 실패: {e}")
                return FAISS.from_texts(["임시 텍스트"], self.embeddings)
        else:
            # 빈 벡터 스토어 생성
            return FAISS.from_texts(["임시 텍스트"], self.embeddings)
    
    def get_vector_store(self):
        """벡터 스토어 반환"""
        return self.vector_store
    
    def get_retriever(self, k=3):
        """검색기 반환"""
        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
    
    def add_texts(self, texts):
        """텍스트를 벡터 스토어에 추가"""
        if len(self.vector_store.docstore._dict) <= 1:  # 임시 텍스트만 있는 경우
            # 새 벡터 스토어 생성
            self.vector_store = FAISS.from_texts(texts, self.embeddings)
        else:
            # 기존 벡터 스토어에 추가
            self.vector_store.add_texts(texts)
        
        # 벡터 스토어 저장
        self.vector_store.save_local(self.store_path)
        
        return self.vector_store
        
    def save(self):
        """벡터 스토어 저장"""
        self.vector_store.save_local(self.store_path)

# 싱글톤 인스턴스 생성
vector_store_service = VectorStoreService() 