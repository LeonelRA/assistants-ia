from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Optional
import os
import re

# Load environment variables
load_dotenv()

# Initialize OpenAI client with beta headers
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    default_headers={"OpenAI-Beta": "assistants=v2"}
)

class Assistant:
    @staticmethod
    async def get_assistants() -> List[Dict]:
        try:
            # Get assistants using v2 API
            response = client.beta.assistants.list()
            return response.data
        except Exception as e:
            raise Exception(f"Error getting assistants from OpenAI: {str(e)}")

    @staticmethod
    async def get_assistant_by_id(assistant_id: str) -> Optional[Dict]:
        try:
            # The retrieve method is not async, so we don't use await
            assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)
            
            if not assistant:
                return None

            response = {
                "id": assistant.id,
                "name": assistant.name,
                "description": assistant.description,
                "model": assistant.model,
                "instructions": assistant.instructions,
                "tools": assistant.tools,
                "tool_resources": assistant.tool_resources if hasattr(assistant, 'tool_resources') else {},
                "created_at": assistant.created_at,
                #"metadata": assistant.metadata or {},
                #"object": assistant.object,
                #"response_format": assistant.response_format if hasattr(assistant, 'response_format') else {"type": "text"},
                #"temperature": assistant.temperature if hasattr(assistant, 'temperature') else 1,
                #"top_p": assistant.top_p if hasattr(assistant, 'top_p') else 1
            }

            return response

        except Exception as e:
            raise Exception(f"Error getting assistant details from OpenAI: {str(e)}")
        
    @staticmethod
    async def create_assistant(name: str, description: str) -> Dict:
        try:
            # 1. Crear vector store
            vector_store = client.vector_stores.create(name=f"{name}_store")

            # 2. Crear asistente con referencia al vector store
            assistant = client.beta.assistants.create(
                name=name,
                description=description,
                model="gpt-4-turbo-preview",
                tools=[{"type": "file_search"}],
                tool_resources={
                    "file_search": {
                        "vector_store_ids": [vector_store.id]
                    }
                }
            )

            # 3. Retornar datos
            return {
                "id": assistant.id,
                "name": assistant.name,
                "description": assistant.description,
                "model": assistant.model,
                "tools": assistant.tools,
                "created_at": assistant.created_at,
                "object": assistant.object,
                "vector_store_id": vector_store.id
            }

        except Exception as e:
            raise Exception(f"Error creating assistant: {str(e)}")

    @staticmethod
    async def update_assistant(
        assistant_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        instructions: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Dict:
        try:
            # Prepare update data
            update_data = {}
            if name is not None:
                update_data["name"] = name
            if description is not None:
                update_data["description"] = description
            if instructions is not None:
                update_data["instructions"] = instructions
            if model is not None:
                update_data["model"] = model

            # Update the assistant
            updated_assistant = client.beta.assistants.update(
                assistant_id=assistant_id,
                **update_data
            )

            # Convert the assistant object to a dictionary
            assistant_dict = {
                "id": updated_assistant.id,
                "name": updated_assistant.name,
                "description": updated_assistant.description,
                "model": updated_assistant.model,
                "instructions": updated_assistant.instructions,
                "created_at": updated_assistant.created_at,
                "object": updated_assistant.object
            }

            return assistant_dict
        except Exception as e:
            raise Exception(f"Error updating assistant: {str(e)}")
        
    @staticmethod
    async def delete_assistant(assistant_id: str) -> None:
        try:

            # Get the assistant
            assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)
            tool_resources = assistant.tool_resources if hasattr(assistant, 'tool_resources') else {}


            if tool_resources:
                vector_store_id = tool_resources.file_search.vector_store_ids[0]
                # Delete the vector store
                client.vector_stores.delete(vector_store_id=vector_store_id)

            # Delete the assistant
            client.beta.assistants.delete(assistant_id=assistant_id)
            
        except Exception as e:
            raise Exception(f"Error deleting assistant: {str(e)}")