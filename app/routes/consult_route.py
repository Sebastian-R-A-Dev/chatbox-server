#consult route logic
from fastapi import APIRouter, HTTPException, Query
from services.consult_service import analyze_question_with_context

router = APIRouter()

@router.get("/consult", tags=["Endpoint to interact directly with the IA model"])
def consult(
    question: str = Query("any question about business logic", description="User's question"),
    language: str = Query("español", description="Language for the answer")
):
    try:
        result = analyze_question_with_context(question, language)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error. Please try again later.")