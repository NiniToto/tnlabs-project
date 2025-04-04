from typing import Dict, Any
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph
from .types import AgentState
from .subgraphs.speech_to_text import speech_to_text_node
from .subgraphs.text_understanding import text_understanding_node
from .subgraphs.calendar_management import calendar_management_node
from .subgraphs.location_management import location_management_node
from .subgraphs.search_management import search_management_node
from ..core.config import settings

def create_agent_graph() -> StateGraph:
    """
    Langgraph 워크플로우를 생성합니다.
    """
    # Groq 모델 초기화
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_MODEL_NAME
    )
    
    # 상태 그래프 초기화
    workflow = StateGraph(AgentState)
    
    # 노드 추가
    workflow.add_node("speech_to_text", speech_to_text_node)
    workflow.add_node("text_understanding", text_understanding_node)
    workflow.add_node("calendar_management", calendar_management_node)
    workflow.add_node("location_management", location_management_node)
    workflow.add_node("search_management", search_management_node)
    
    # 엣지 추가
    workflow.add_edge("speech_to_text", "text_understanding")
    workflow.add_conditional_edges(
        "text_understanding",
        lambda x: x["action_type"],
        {
            "calendar": "calendar_management",
            "location": "location_management",
            "search": "search_management"
        }
    )
    
    # 시작 노드 설정
    workflow.set_entry_point("speech_to_text")
    
    # 그래프 컴파일
    return workflow.compile() 