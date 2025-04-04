from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.models.schema import ChatMessage, ChatRequest, ChatResponse, DocumentResponse
from app.services.rag_service import rag_service
from app.services.document_service import document_service
from typing import List
import tempfile
import os
from ..graphs.main_graph import create_agent_graph
from ..graphs.types import AgentState
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel
from ..graphs.subgraphs.text_understanding import text_understanding_node

router = APIRouter()

# Langgraph 워크플로우 초기화
workflow = create_agent_graph()

# 텍스트 입력을 위한 Pydantic 모델
class TextInput(BaseModel):
    text: str

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

@router.post("/process-audio")
async def process_audio(audio_file: UploadFile = File(...)):
    """
    음성 파일을 처리하고 적절한 응답을 반환하는 엔드포인트
    """
    try:
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # 초기 상태 설정
        initial_state = AgentState(
            messages=[],
            audio_input=temp_file_path,
            text_input="",
            action_type="",
            action_data={}
        )
        
        # 워크플로우 실행
        final_state = workflow.invoke(initial_state)
        
        # 임시 파일 삭제
        os.unlink(temp_file_path)
        
        # 응답 생성
        response = {
            "messages": [
                {
                    "role": "user" if isinstance(msg, HumanMessage) else "assistant",
                    "content": msg.content
                }
                for msg in final_state["messages"]
            ]
        }
        
        return response
        
    except Exception as e:
        return {"error": str(e)}

@router.post("/analyze-text")
async def analyze_text(text_input: TextInput):
    """
    텍스트를 분석하여 어떤 API를 호출해야 하는지 결정하는 엔드포인트
    """
    try:
        # 초기 상태 설정
        initial_state = AgentState(
            messages=[],
            audio_input="",
            text_input=text_input.text,
            action_type="",
            action_data={}
        )
        
        # 텍스트 이해 노드 실행
        final_state = text_understanding_node(initial_state)
        
        # 응답 생성
        response = {
            "action_type": final_state["action_type"],
            "action_data": final_state["action_data"],
            "messages": [
                {
                    "role": "user" if isinstance(msg, HumanMessage) else "assistant",
                    "content": msg.content
                }
                for msg in final_state["messages"]
            ]
        }
        
        return response
        
    except Exception as e:
        return {"error": str(e)}

