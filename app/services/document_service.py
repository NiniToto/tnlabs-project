import os
from typing import List, BinaryIO
import tempfile
from app.services.rag_service import rag_service

class DocumentService:
    """문서 처리 서비스"""
    
    def __init__(self):
        """문서 처리 서비스 초기화"""
        self.supported_formats = ['.txt', '.pdf', '.docx']
    
    def process_text_file(self, file_content: str) -> str:
        """텍스트 파일 처리"""
        return file_content
    
    async def process_file(self, file: BinaryIO, filename: str) -> dict:
        """
        파일을 처리하고 벡터 스토어에 추가
        현재는 텍스트 파일만 지원함
        """
        try:
            # 파일 확장자 확인
            _, file_extension = os.path.splitext(filename)
            
            if file_extension.lower() not in self.supported_formats:
                return {
                    "success": False,
                    "message": f"지원하지 않는 파일 형식입니다. 지원 형식: {', '.join(self.supported_formats)}"
                }
            
            # 현재는 텍스트 파일만 구현
            if file_extension.lower() == '.txt':
                # 파일 내용 읽기
                file_content = file.read().decode('utf-8')
                processed_text = self.process_text_file(file_content)
                
                # RAG 시스템에 추가
                rag_service.add_documents([processed_text])
                
                return {
                    "success": True,
                    "message": f"파일 '{filename}'이(가) 성공적으로 처리되었습니다."
                }
            else:
                # 향후 PDF, DOCX 등 추가 지원 예정
                return {
                    "success": False,
                    "message": f"파일 형식 '{file_extension}'은 아직 구현 중입니다."
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"파일 처리 중 오류 발생: {str(e)}"
            }

# 싱글톤 인스턴스 생성
document_service = DocumentService()