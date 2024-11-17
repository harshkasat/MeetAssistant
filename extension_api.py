from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import re
from typing import ClassVar
import logging
from enum import Enum

from main import google_meet

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pydantic models for request/response validation
class MeetingRequest(BaseModel):
    meetUrl: str

    @field_validator('meetUrl')
    def validate_meet_url(cls, v):
        if not re.match(r'^https://meet\.google\.com/[a-z]{3}-[a-z]{4}-[a-z]{3}$', v):
            raise ValueError('Invalid Google Meet URL format')
        return v
class StatusEnum(str, Enum):
    SUCCESS = "success"

class MeetingResponse(BaseModel):
    status: StatusEnum 
    message: str
    ERROR: ClassVar[str] = "error"

# Initialize FastAPI app
app = FastAPI(
    title="Meet Bot API",
    description="API for managing Google Meet bot instances",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/new-meeting", )
async def new_meeting(request: MeetingRequest):
    """
    Handle new meeting requests from the Chrome extension.
    
    - Validates the meeting URL format
    - Ensures no duplicate processing
    - Initiates bot joining process
    """
    try:
        success = await google_meet(request.meetUrl)
        
        if success:
            return MeetingResponse(
                status=StatusEnum.SUCCESS,
                message="Bot initiated successfully"
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Meeting is already being processed"
            )
            
    except Exception as e:
        logger.error(f"Error handling new meeting: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")