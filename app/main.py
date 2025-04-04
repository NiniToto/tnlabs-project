from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes

app = FastAPI(
    title="RAG 챗봇 API",
    description="LangChain과 Groq를 이용한 RAG 챗봇 API",
    version="0.1.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(routes.router)

@app.get("/")
async def root():
    return {"message": "RAG 챗봇 API에 오신 것을 환영합니다!"}   





