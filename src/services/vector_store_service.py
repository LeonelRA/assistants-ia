from fastapi import HTTPException, UploadFile, File
from typing import List
from src.crud.assistant import Assistant
from src.crud.vector_store import VectorStore

class VectorStoreService:

    @staticmethod
    async def get_vector_store_id(assistant: dict) -> str:
        tool_resources = assistant.get('tool_resources')
        
        if tool_resources and tool_resources.file_search:
            vector_store_ids = tool_resources.file_search.vector_store_ids
            vector_store_id = vector_store_ids[0] if vector_store_ids else None
            
            if vector_store_id:
                return vector_store_id
                
        raise HTTPException(status_code=404, detail="Vector store not found for this assistant")

    @staticmethod
    async def get_assistant_files(assistant_id: str):
        try:
            # Obtener el asistente para obtener el vector_store_id
            assistant = await Assistant.get_assistant_by_id(assistant_id)

            if not assistant:
                raise HTTPException(status_code=404, detail="Assistant not found")
            
            # Obtener el vector_store_id del asistente
            vector_store_id = await VectorStoreService.get_vector_store_id(assistant)
            
            # Obtener los archivos del vector store
            files = await VectorStore.get_vector_store_files(vector_store_id)
            return files
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def add_file_to_assistant(assistant_id: str, files: List[UploadFile] = File(...)):
        try:
            # Obtener el asistente para obtener el vector_store_id
            assistant = await Assistant.get_assistant_by_id(assistant_id)

            if not assistant:
                raise HTTPException(status_code=404, detail="Assistant not found")
            
            # Obtener el vector_store_id del asistente
            vector_store_id = await VectorStoreService.get_vector_store_id(assistant)


            if not vector_store_id:
                raise HTTPException(status_code=404, detail="Vector store not found for this assistant")
            
            # Procesar cada archivo
            for file in files:
                # Validar tipo de archivo
                if not file.filename.endswith(('.pdf', '.txt')):
                    raise HTTPException(
                        status_code=400,
                        detail=f"File {file.filename} is not a PDF or TXT file"
                    )
                
                # Agregar el archivo al vector store
                await VectorStore.add_file_to_vector_store(
                    vector_store_id=vector_store_id,
                    file=file
                )
            
            # Obtener la lista actualizada de archivos
            updated_files = await VectorStore.get_vector_store_files(vector_store_id)
            return {"files": updated_files}
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def delete_file_from_assistant(assistant_id: str, file_id: str):
        try:
            # Obtener el asistente para obtener el vector_store_id
            assistant = await Assistant.get_assistant_by_id(assistant_id)
            if not assistant:
                raise HTTPException(status_code=404, detail="Assistant not found")
            
            # Obtener el vector_store_id del asistente
            vector_store_id = await VectorStoreService.get_vector_store_id(assistant)
            
            # Eliminar el archivo del vector store
            await VectorStore.delete_file_from_vector_store(vector_store_id, file_id)
            
            return {"message": "File deleted successfully"}
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 