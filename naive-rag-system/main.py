from fastapi import FastAPI 
from src.api.v1.routes.query import router as query_router

def main():
    pass
app = FastAPI(title="RAG API")

app.include_router(query_router, prefix="/api/v1")
if __name__ == "__main__":
    main()
