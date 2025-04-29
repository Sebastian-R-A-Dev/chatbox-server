# testing route
from fastapi import APIRouter, HTTPException, Query
from services.test_service import test_ollama_connection, service_is_ready

router = APIRouter()

@router.get("/status", tags=["Test if service is running"])
def service_status():
    return service_is_ready()

@router.get("/ollama-status", tags=["Test ollama connection"])
def test_ollama_status():
    return test_ollama_connection()