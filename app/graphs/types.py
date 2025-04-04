from typing import TypedDict, List, Dict, Any
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """에이전트 상태를 나타내는 타입"""
    messages: List[BaseMessage]
    audio_input: str
    text_input: str
    action_type: str
    action_data: Dict[str, Any] 