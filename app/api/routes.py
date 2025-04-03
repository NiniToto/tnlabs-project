from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.models.schema import ChatMessage, ChatRequest, ChatResponse, DocumentResponse
from app.services.rag_service import rag_service
from app.services.document_service import document_service
from typing import List

router = APIRouter()

@router.get("/health")
async def health_check():
    """헬스 체크 API"""
    return {"message": "HEALTH CHECK"}

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """RAG 챗봇과 대화하기 API"""
    # 마지막 메시지가 사용자 메시지인지 확인
    if not request.messages or request.messages[-1].role != "user":
        raise HTTPException(status_code=400, detail="마지막 메시지는 사용자 메시지여야 합니다")
    
    # 쿼리 추출
    query = request.query or request.messages[-1].content
    
    # 이전 대화 기록 변환
    chat_history = []
    for i in range(0, len(request.messages) - 1, 2):
        if i + 1 < len(request.messages) and request.messages[i].role == "user" and request.messages[i+1].role == "assistant":
            chat_history.append((request.messages[i].content, request.messages[i+1].content))
    
    # RAG 챗봇 응답 생성
    result = rag_service.chat(query, chat_history)
    
    return {"response": result["response"]}

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """문서 업로드 및 처리 API"""
    # 파일 처리
    result = await document_service.process_file(file.file, file.filename)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return {"success": result["success"], "message": result["message"]}

