import speech_recognition as sr
from ..types import AgentState
from langchain_core.messages import HumanMessage

def speech_to_text_node(state: AgentState) -> AgentState:
    """
    음성을 텍스트로 변환하는 노드
    """
    # 음성 인식기 초기화
    recognizer = sr.Recognizer()
    
    try:
        # 오디오 파일을 텍스트로 변환
        with sr.AudioFile(state["audio_input"]) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language='ko-KR')
            
            # 상태 업데이트
            state["text_input"] = text
            state["messages"].append(HumanMessage(content=text))
            
            return state
            
    except Exception as e:
        print(f"Error in speech to text conversion: {str(e)}")
        state["text_input"] = ""
        return state 