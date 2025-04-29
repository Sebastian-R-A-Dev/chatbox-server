#main file logic
from fastapi import FastAPI
from app.routes import consult_route, test_route

app = FastAPI()

app.include_router(consult_route.router, prefix="/api", tags=["Route for consult endpoints"])
app.include_router(test_route.router, prefix="/api", tags=["Route for test endpoints"])