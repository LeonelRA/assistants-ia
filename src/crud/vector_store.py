from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import UploadFile
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client with beta headers
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    default_headers={"OpenAI-Beta": "assistants=v2"}
)

class VectorStore:
    @staticmethod
    async def get_vector_store_files(vector_store_id: str) -> List[Dict]:
        try:
            # Get files from vector store using the full API path
            response = client.vector_stores.files.list(vector_store_id=vector_store_id)

            files = []
            for file in response.data:
                files.append({
                    "id": file.id,
                    "filename": client.files.retrieve(file.id).filename,
                    "object": file.object,
                    "created_at": file.created_at,
                    "status": file.status,
                    "usage_bytes": file.usage_bytes,
                })

            # Convert VectorStoreFile objects to dictionaries
            return files
        
        except Exception as e:
            raise Exception(f"Error getting vector store files: {str(e)}")
    
    @staticmethod
    async def add_file_to_vector_store(vector_store_id: str, file: UploadFile) -> Dict:
        try:
            # Leer el contenido del archivo
            file_content = await file.read()
            
            # Crear un archivo en OpenAI
            openai_file = client.files.create(
                file=(file.filename, file_content, file.content_type),
                purpose="assistants"
            )
            
            # Asociar el archivo con la tienda de vectores
            vector_store_file = client.vector_stores.files.create(
                vector_store_id=vector_store_id,
                file_id=openai_file.id
            )
            
            return {
                "id": vector_store_file.id,
                "file_id": openai_file.id,
                "filename": file.filename,
                "vector_store_id": vector_store_id,
                "status": vector_store_file.status,
                "created_at": vector_store_file.created_at
            }
        except Exception as e:
            raise Exception(f"Error al agregar archivo a la tienda de vectores: {str(e)}")
        
    @staticmethod
    async def delete_file_from_vector_store(vector_store_id: str, file_id: str) -> None:
        try:
            # Delete the file from the vector store
            client.vector_stores.files.delete(
                vector_store_id=vector_store_id,
                file_id=file_id
            )
        except Exception as e:
            raise Exception(f"Error deleting file from vector store: {str(e)}")

