from fastapi import APIRouter, UploadFile, File
from typing import List
from src.services.vector_store_service import VectorStoreService

router = APIRouter(prefix="/vector-stores", tags=["vector-stores"])

# Obtener los archivos de un asistente específico
@router.get("/{assistant_id}/files")
async def get_assistant_files_route(assistant_id: str):
    return await VectorStoreService.get_assistant_files(assistant_id)

# Agregar archivos a un asistente específico
@router.post("/{assistant_id}/files")
async def add_file_to_assistant_route(
    assistant_id: str,
    files: List[UploadFile] = File(...)
):
    return await VectorStoreService.add_file_to_assistant(assistant_id, files)

@router.delete("/{assistant_id}/files/{file_id}")
async def delete_file_from_assistant_route(assistant_id: str, file_id: str):
    return await VectorStoreService.delete_file_from_assistant(assistant_id, file_id) 