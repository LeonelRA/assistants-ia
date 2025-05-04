from src.services.chat_service import ChatService
from src.services.vector_store_service import VectorStoreService
from src.models.assistant import UpdateAssistantRequest
from src.crud.assistant import Assistant
from fastapi import HTTPException

class AssistantService:
    @staticmethod
    async def get_assistants():
        try:
            assistants = await Assistant.get_assistants()
            return {"assistants": assistants}
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_data_assistant(assistant_id: str):
        try:
            assistant = await Assistant.get_assistant_by_id(assistant_id)

            if assistant is None:
                raise HTTPException(status_code=404, detail="Assistant not found")

            assistant_files = await VectorStoreService.get_assistant_files(assistant_id)

            if assistant_files:
                assistant['files'] = assistant_files

            return {"assistant": assistant}
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    async def create_assistant(
        name: str,
        description: str
    ):
        try:
            assistant = await Assistant.create_assistant(
                name=name,
                description=description
            )
            return {"assistant": assistant}
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    async def update_assistant(assistant_id: str, request: UpdateAssistantRequest):
        try:
            # Convertir el modelo Pydantic a un diccionario y filtrar los campos None
            update_data = request.dict(exclude_none=True)
            # Llamar al servicio con los datos filtrados
            updated_assistant = await Assistant.update_assistant(
                assistant_id=assistant_id,
                **update_data
            )
            return {"assistant": updated_assistant}
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        

    @staticmethod
    async def delete_assistant(assistant_id: str):
        try:
            # Verificar si el asistente existe antes de eliminarlo
            assistant = await Assistant.get_assistant_by_id(assistant_id)
            if not assistant:
                raise HTTPException(status_code=404, detail="Assistant not found")
                
            # Eliminar el asistente
            await Assistant.delete_assistant(assistant_id)
            return {
                "message": "Assistant deleted successfully",
                "assistant_id": assistant_id
            }
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error deleting assistant: {str(e)}"
            )