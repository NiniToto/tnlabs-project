import requests
from typing import Dict
from langchain_core.messages import AIMessage
from ..main_graph import AgentState
from ...core.config import settings

def calendar_management_node(state: AgentState) -> AgentState:
    """
    네이버 캘린더 API를 사용하여 일정을 관리하는 노드
    """
    action_data = state["action_data"]
    
    # 네이버 캘린더 API 엔드포인트
    calendar_api_url = "https://openapi.naver.com/v1/calendar"
    
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
        "Content-Type": "application/json"
    }
    
    try:
        # 일정 데이터 준비
        calendar_data = {
            "summary": action_data.get("title", ""),
            "description": action_data.get("description", ""),
            "start": {
                "dateTime": action_data.get("start_time", ""),
                "timeZone": "Asia/Seoul"
            },
            "end": {
                "dateTime": action_data.get("end_time", ""),
                "timeZone": "Asia/Seoul"
            }
        }
        
        # API 호출
        response = requests.post(
            calendar_api_url,
            headers=headers,
            json=calendar_data
        )
        
        if response.status_code == 200:
            result = response.json()
            state["messages"].append(
                AIMessage(content=f"일정이 성공적으로 추가되었습니다: {result}")
            )
        else:
            state["messages"].append(
                AIMessage(content=f"일정 추가 실패: {response.text}")
            )
            
    except Exception as e:
        state["messages"].append(
            AIMessage(content=f"캘린더 관리 중 오류 발생: {str(e)}")
        )
    
    return state 