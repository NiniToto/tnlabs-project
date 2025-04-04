import requests
from typing import Dict
from langchain_core.messages import AIMessage
from ..main_graph import AgentState
from ...core.config import settings

def location_management_node(state: AgentState) -> AgentState:
    """
    네이버 지도 API를 사용하여 위치를 관리하는 노드
    """
    action_data = state["action_data"]
    
    # 네이버 지도 API 엔드포인트
    map_api_url = "https://openapi.naver.com/v1/map/geocode"
    
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET
    }
    
    try:
        # 위치 검색
        params = {
            "query": action_data.get("location", ""),
            "coordinate": "latlng"
        }
        
        response = requests.get(
            map_api_url,
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("result", {}).get("total", 0) > 0:
                location = result["result"]["items"][0]
                
                # 위치 정보 저장
                location_data = {
                    "name": location.get("title", ""),
                    "address": location.get("address", ""),
                    "latitude": location.get("point", {}).get("y", ""),
                    "longitude": location.get("point", {}).get("x", ""),
                    "map_url": f"https://map.naver.com/v5/search/{action_data.get('location', '')}"
                }
                
                state["messages"].append(
                    AIMessage(content=f"위치를 찾았습니다: {location_data}")
                )
                
                # 캘린더에 위치 정보가 포함된 일정 추가가 필요한 경우
                if action_data.get("add_to_calendar", False):
                    state["action_type"] = "calendar"
                    state["action_data"].update({
                        "title": f"{action_data.get('title', '')} - {location_data['name']}",
                        "description": f"위치: {location_data['address']}\n지도: {location_data['map_url']}"
                    })
            else:
                state["messages"].append(
                    AIMessage(content="위치를 찾을 수 없습니다.")
                )
        else:
            state["messages"].append(
                AIMessage(content=f"위치 검색 실패: {response.text}")
            )
            
    except Exception as e:
        state["messages"].append(
            AIMessage(content=f"위치 관리 중 오류 발생: {str(e)}")
        )
    
    return state 