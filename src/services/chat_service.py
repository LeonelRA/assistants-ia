from dotenv import load_dotenv
from openai import OpenAI
from fastapi import HTTPException, UploadFile
import os
import re
import tempfile
import httpx

# Load environment variables
load_dotenv()

# Initialize OpenAI client with beta headers
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    default_headers={"OpenAI-Beta": "assistants=v2"}
)

class ChatService:
    @staticmethod
    async def chat_with_assistant(assistant_id: str, message: str = None, audio: UploadFile = None) -> str:
        try:
            # Si hay audio, transcribirlo
            if audio:
                # Validar tipo de archivo
                if not audio.content_type.startswith('audio/'):
                    raise HTTPException(
                        status_code=400,
                        detail="El archivo debe ser de tipo audio"
                    )
                
                # Guardar el archivo temporalmente
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                    content = await audio.read()
                    temp_file.write(content)
                    temp_file_path = temp_file.name
                
                try:
                    # Transcribir el audio
                    with open(temp_file_path, "rb") as audio_file:
                        transcript = client.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio_file
                        )
                    message = transcript.text
                finally:
                    # Limpiar el archivo temporal
                    os.unlink(temp_file_path)
            
            # Verificar que tenemos un mensaje
            if not message:
                raise HTTPException(
                    status_code=400,
                    detail="No se pudo obtener el mensaje del audio"
                )
            
            # Create a thread
            thread = client.beta.threads.create()
            
            # Add message to thread
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=message
            )
            
            # Run the assistant
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id
            )
            
            # Wait for the run to complete
            while True:
                run_status = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                if run_status.status == 'completed':
                    break
                elif run_status.status in ['failed', 'cancelled', 'expired']:
                    raise Exception(f"Run failed with status: {run_status.status}")
            
            # Get the assistant's response
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            assistant_message = next(
                (msg for msg in messages.data if msg.role == "assistant"),
                None
            )
            
            if not assistant_message:
                raise Exception("No response from assistant")
            
            # Limpiar referencias tipo 【n:m†archivo.txt】
            cleaned_response = re.sub(r"【\d+:\d+†[^】]+】", "", assistant_message.content[0].text.value)

            return {"message": cleaned_response}
            
        except HTTPException as he:
            raise he
        except Exception as e:
            error_message = f"Error al chatear con el asistente: {str(e)}"
            print(f"Error detallado: {error_message}")  # Para logging
            raise HTTPException(
                status_code=500,
                detail=error_message
            )


    @staticmethod
    async def get_session_realtime(assistant_id: str):
        try:
            # Obtener la información del asistente
            assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)

            # Hacer una solicitud POST personalizada al endpoint
            response = client.post(
                "/realtime/sessions",
                cast_to=httpx.Response,
                body={
                    "model": "gpt-4o-realtime-preview-2024-12-17",
                    "instructions": assistant.instructions,
                },
            )
            # Obtener los datos en formato JSON
            data = response.json()
            return data
        except HTTPException as he:
            raise he
        except Exception as error:
            print(f"Error in /session-realtime: {error}")
            raise HTTPException(
                status_code=500,
                detail="Internal Server Error"
            )