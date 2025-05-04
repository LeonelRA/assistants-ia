from pydantic import BaseModel
from typing import Optional, List, Dict
from fastapi import UploadFile

class UpdateAssistantRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    model: Optional[str] = None

class UpdateAssistantFilesRequest(BaseModel):
    file: UploadFile
