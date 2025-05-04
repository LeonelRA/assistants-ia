from fastapi import APIRouter, HTTPException, UploadFile, File, Body, Form
from typing import List, Dict, Optional
from src.services.chat_service import ChatService
from src.services.vector_store_service import VectorStoreService
from src.services.assistant_service import AssistantService
from src.models.assistant import UpdateAssistantRequest
import json
import base64
import tempfile
import os
from openai import OpenAI
from dotenv import load_dotenv
import io
import wave
import struct
import numpy as np

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter(prefix="/assistants", tags=["assistants"])

# Obtener todos los asistentes
@router.get("")
async def get_assistants_route():
    return await AssistantService.get_assistants()

# Obtener un asistente específico
@router.get("/{assistant_id}")
async def get_data_assistant_route(assistant_id: str):
    return await AssistantService.get_data_assistant(assistant_id)


# Crear un nuevo asistente
@router.post("")
async def create_assistant_route(
    name: str = Body(...),
    description: str = Body(...)
):
    return await AssistantService.create_assistant(name, description)
   

# Actualizar un asistente específico
@router.put("/{assistant_id}")
async def update_assistant_route(assistant_id: str, request: UpdateAssistantRequest):
    return await AssistantService.update_assistant(assistant_id, request)

# Eliminar un asistente específico
@router.delete("/{assistant_id}")
async def delete_assistant_route(assistant_id: str):
    return await AssistantService.delete_assistant(assistant_id)
        

# Chatear con un asistente específico
@router.post("/{assistant_id}/chat")
async def chat_with_assistant(
    assistant_id: str,
    message: Optional[str] = Form(None),
    audio: Optional[UploadFile] = File(None)
):
    if not message and not audio:
        raise HTTPException(
            status_code=400,
            detail="Debe proporcionar un mensaje de texto o un archivo de audio"
        )
    
    if message and audio:
        raise HTTPException(
            status_code=400,
            detail="No puede enviar texto y audio al mismo tiempo"
        )
    
    return await ChatService.chat_with_assistant(assistant_id, message, audio)

