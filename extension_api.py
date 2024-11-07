from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, field_validator
import re
import threading
from typing import Set
import logging
import time
from enum import Enum

from google_meet import google_meet

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
    ERROR = "error"

class MeetingResponse(BaseModel):
    status: StatusEnum
    message: str

class MeetingManager:
    def __init__(self):
        self.bot = None
        self.active_meetings: Set[str] = set()
        self.lock = threading.Lock()  # Thread-safe operations
    
    async def handle_new_meeting(self, meet_url: str) -> bool:
        with self.lock:
            if meet_url in self.active_meetings:
                logger.info(f"Meeting already being processed: {meet_url}")
                return False
            
            self.active_meetings.add(meet_url)
            logger.info(f"Added new meeting: {meet_url}")
        
        # Start bot in a separate thread
        threading.Thread(
            target=self._process_meeting,
            args=(meet_url,),
            daemon=True
        ).start()
        
        return True
    
    def _process_meeting(self, meet_url: str):
        try:
            logger.info(f"Starting to process meeting: {meet_url}")
            if not self.bot:
                google_meet(meet_url)
            else:
                logger.error(f"Failed to join meeting: {meet_url}")
        
        except Exception as e:
            logger.error(f"Error processing meeting {meet_url}: {str(e)}", exc_info=True)
        
        finally:
            with self.lock:
                self.active_meetings.remove(meet_url)
                logger.info(f"Removed meeting from active set: {meet_url}")

    async def get_active_meetings(self) -> Set[str]:
        """Get current active meetings"""
        with self.lock:
            return self.active_meetings.copy()

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

# Initialize meeting manager
meeting_manager = MeetingManager()

@app.post("/new-meeting", response_model=MeetingResponse)
async def new_meeting(request: MeetingRequest):
    """
    Handle new meeting requests from the Chrome extension.
    
    - Validates the meeting URL format
    - Ensures no duplicate processing
    - Initiates bot joining process
    """
    try:
        success = await meeting_manager.handle_new_meeting(request.meetUrl)
        
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

@app.get("/active-meetings", response_model=Set[str])
async def get_active_meetings():
    """Get list of currently active meetings"""
    return await meeting_manager.get_active_meetings()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/leave-meeting")
async def leave_meeting():
    """Leave meeting"""
    google_meet(leave_meet=True)
    return {"status": "success"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")