from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ChatMessage(BaseModel):
    """채팅 메시지 모델"""
    role: str
    content: str

class ChatRequest(BaseModel):
    """채팅 요청 모델"""
    messages: List[ChatMessage]
    context: Optional[str] = None
    query: Optional[str] = None

class ChatResponse(BaseModel):
    """채팅 응답 모델"""
    response: str

class DocumentResponse(BaseModel):
    """문서 처리 응답 모델"""
    success: bool
    message: str 