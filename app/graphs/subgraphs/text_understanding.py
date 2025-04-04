from typing import Dict
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from ..main_graph import AgentState
from ...core.config import settings

def text_understanding_node(state: AgentState) -> AgentState:
    """
    텍스트를 이해하고 적절한 액션을 결정하는 노드
    """
    llm = ChatGroq(
        model_name=settings.GROQ_MODEL_NAME,
        temperature=0.7
    )
    
    # 시스템 프롬프트
    system_prompt = """당신은 사용자의 텍스트를 분석하여 적절한 액션을 결정하는 AI 어시스턴트입니다.
    다음 액션 중 하나를 선택해야 합니다:
    - calendar: 일정 관리가 필요한 경우
    - location: 위치 검색이나 지도 관련 작업이 필요한 경우
    - search: 일반적인 검색이 필요한 경우
    
    응답은 다음 형식이어야 합니다:
    {
        "action_type": "calendar|location|search",
        "action_data": {
            // 액션에 필요한 구체적인 데이터
        }
    }
    """
    
    # 사용자 메시지와 시스템 프롬프트 결합
    messages = [
        HumanMessage(content=system_prompt),
        HumanMessage(content=state["text_input"])
    ]
    
    # LLM에 질문
    response = llm.invoke(messages)
    
    try:
        # 응답 파싱
        import json
        action_data = json.loads(response.content)
        
        # 상태 업데이트
        state["action_type"] = action_data["action_type"]
        state["action_data"] = action_data["action_data"]
        state["messages"].append(AIMessage(content=response.content))
        
    except Exception as e:
        print(f"Error in text understanding: {str(e)}")
        state["action_type"] = "search"  # 기본값
        state["action_data"] = {"query": state["text_input"]}
    
    return state 