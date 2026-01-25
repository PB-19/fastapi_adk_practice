import os
import uvicorn
from backend.app import app

if __name__=="__main__":
    uvicorn.run(
        "main:app", 
        host=os.getenv("DEFAULT_API_HOST"), 
        port=int(os.getenv("DEFAULT_API_PORT")),
        reload=True,
    )