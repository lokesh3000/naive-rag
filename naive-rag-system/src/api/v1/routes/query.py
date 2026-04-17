from fastapi import APIRouter
from src.core.db import get_vector_store
from src.api.v1.services.query_service import query_documents
from src.api.v1.schemas.query_schema import QueryRequest, QueryResponse

router = APIRouter()

@router.post("/query", response_model = QueryResponse)
def query_endpoint(request: QueryRequest):
    # vector_store = get_vector_store()

    # docs = vector_store.similarity_search(request.query, k=5)

    results = query_documents(request.query, k=5)
    return QueryResponse(query=request.query, results=results)

    # return {
    #     "query": request.query,
    #     "results": [
    #         {
    #             "content": doc.page_content,
    #             "metadata": doc.metadata
    #         }
    #         for doc in docs
    #     ]
    # }