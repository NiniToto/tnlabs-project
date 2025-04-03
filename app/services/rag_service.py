from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.services.llm_service import llm_service
from app.services.vector_store_service import vector_store_service
from typing import List, Dict, Any, Optional

class RAGService:
    """RAG 서비스"""
    
    def __init__(self):
        """RAG 서비스 초기화"""
        self.llm = llm_service.get_llm()
        self.retriever = vector_store_service.get_retriever(k=3)
        self.qa_template = self._create_qa_template()
        self.conversation_chain = self._create_conversation_chain()
    
    def _create_qa_template(self):
        """QA 프롬프트 템플릿 생성"""
        template = """
        다음은 문서에서 추출한 관련 정보입니다:
        {context}
        
        이를 바탕으로 다음 질문에 답변해주세요: {question}
        
        대화 기록:
        {chat_history}
        """
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question", "chat_history"]
        )
    
    def _create_conversation_chain(self):
        """대화 체인 생성"""
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": self.qa_template}
        )
    
    def add_documents(self, texts: List[str]):
        """문서를 분할하고 벡터 스토어에 추가"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        chunks = text_splitter.split_text("\n".join(texts))
        
        # 청크가 있는 경우 벡터 스토어에 추가
        if chunks:
            vector_store_service.add_texts(chunks)
            
            # 검색기 업데이트
            self.retriever = vector_store_service.get_retriever(k=3)
            
            # 대화 체인 업데이트
            self.conversation_chain = self._create_conversation_chain()
    
    def chat(self, query: str, chat_history: List = None):
        """사용자 쿼리에 대해 RAG 응답을 생성"""
        if chat_history is None:
            chat_history = []
            
        try:
            # ConversationalRetrievalChain을 이용한 응답 생성
            result = self.conversation_chain.invoke({
                "question": query,
                "chat_history": chat_history
            })
            
            # 응답 추출
            response = result.get("answer", "답변을 생성할 수 없습니다.")
            
            # 대화 기록 업데이트
            chat_history.append((query, response))
            
            return {
                "response": response,
                "source_documents": result.get("source_documents", [])
            }
        except Exception as e:
            return {
                "response": f"오류가 발생했습니다: {str(e)}",
                "source_documents": []
            }

# 싱글톤 인스턴스 생성
rag_service = RAGService() 