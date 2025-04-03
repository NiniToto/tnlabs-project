from fastapi import FastAPI
from app.api import routes
from app.core.config import setup_cors

app = FastAPI(
    title="RAG 챗봇 API",
    description="LangChain과 Groq를 이용한 RAG 챗봇 API",
    version="0.1.0"
)

# CORS 설정  
setup_cors(app)

# 라우터 등록
app.include_router(routes.router)

@app.get("/")
async def root():
    return {"message": "RAG 챗봇 API에 오신 것을 환영합니다!"}   





