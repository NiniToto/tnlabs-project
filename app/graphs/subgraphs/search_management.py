import requests
from typing import Dict
from langchain_core.messages import AIMessage
from ..main_graph import AgentState
from ...core.config import settings

def search_management_node(state: AgentState) -> AgentState:
    """
    네이버 검색 API를 사용하여 검색을 수행하는 노드
    """
    action_data = state["action_data"]
    
    # 네이버 검색 API 엔드포인트
    search_api_url = "https://openapi.naver.com/v1/search/blog"
    
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET
    }
    
    try:
        # 검색 파라미터 설정
        params = {
            "query": action_data.get("query", ""),
            "display": 5,  # 검색 결과 개수
            "sort": "sim"  # 정확도순 정렬
        }
        
        # API 호출
        response = requests.get(
            search_api_url,
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("total", 0) > 0:
                # 검색 결과 요약
                search_results = []
                for item in result["items"]:
                    search_results.append({
                        "title": item.get("title", "").replace("<b>", "").replace("</b>", ""),
                        "link": item.get("link", ""),
                        "description": item.get("description", "").replace("<b>", "").replace("</b>", "")
                    })
                
                # 결과 메시지 생성
                result_message = "검색 결과:\n\n"
                for i, item in enumerate(search_results, 1):
                    result_message += f"{i}. {item['title']}\n"
                    result_message += f"   {item['description']}\n"
                    result_message += f"   링크: {item['link']}\n\n"
                
                state["messages"].append(
                    AIMessage(content=result_message)
                )
            else:
                state["messages"].append(
                    AIMessage(content="검색 결과가 없습니다.")
                )
        else:
            state["messages"].append(
                AIMessage(content=f"검색 실패: {response.text}")
            )
            
    except Exception as e:
        state["messages"].append(
            AIMessage(content=f"검색 중 오류 발생: {str(e)}")
        )
    
    return state 