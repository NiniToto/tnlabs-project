# RAG 챗봇 프로젝트

랭체인(LangChain)과 Groq API를 이용한 RAG(Retrieval-Augmented Generation) 챗봇 구현 프로젝트입니다.

## 주요 기능

- Groq API를 이용한 LLM 엔진 활용
- HuggingFace의 다국어 임베딩 모델 적용
- 문서 업로드 및 벡터 데이터베이스 저장
- RAG 기반 대화형 챗봇 인터페이스

## 기술 스택

- **백엔드**: FastAPI
- **LLM**: Groq API (llama3-70b-8192)
- **임베딩**: HuggingFace (sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
- **벡터 스토어**: FAISS

## 프로젝트 구조

```
app/
  ├── api/              # API 엔드포인트
  │   ├── __init__.py
  │   └── routes.py
  ├── core/             # 핵심 설정 및 유틸리티
  │   ├── __init__.py
  │   └── config.py
  ├── models/           # 데이터 모델
  │   ├── __init__.py
  │   └── schema.py
  ├── services/         # 비즈니스 로직 서비스
  │   ├── __init__.py
  │   ├── document_service.py
  │   ├── embedding_service.py
  │   ├── llm_service.py
  │   ├── rag_service.py
  │   └── vector_store_service.py
  ├── utils/            # 유틸리티 함수
  │   └── __init__.py
  ├── __init__.py
  └── main.py           # 애플리케이션 진입점
```

## 시작하기

### 환경 설정

1. 가상 환경 생성 및 활성화
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

2. 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```

3. .env 파일 생성 및 환경 변수 설정
   ```
   # .env 파일 내용
   GROQ_API_KEY=your_groq_api_key
   LLM_MODEL=llama3-70b-8192
   EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
   VECTOR_STORE_PATH=data/vector_store
   ```

### 서버 실행

```bash
uvicorn app.main:app --reload
```

## API 엔드포인트

- **GET /**: 기본 환영 메시지
- **GET /health**: 헬스 체크
- **POST /chat**: 챗봇과 대화
- **POST /upload**: 문서 업로드

## 사용 예시

### 챗봇 대화

```python
import requests
import json

url = "http://localhost:8000/chat"
payload = {
    "messages": [
        {"role": "user", "content": "안녕하세요?"}
    ]
}
headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.json())
```

### 문서 업로드

```python
import requests

url = "http://localhost:8000/upload"
files = {'file': open('sample.txt', 'rb')}

response = requests.post(url, files=files)
print(response.json())
```

## 향후 개발 계획

- PDF, DOCX 파일 지원 추가
- 웹 인터페이스 개발
- 다중 임베딩 모델 지원

## 라이센스

MIT 