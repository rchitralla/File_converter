import asyncio
import websockets
from moviepy.editor import AudioFileClip
import tempfile
import base64

async def convert_audio(websocket, path):
    try:
        # Receive base64-encoded audio file content
        audio_content_base64 = await websocket.recv()
        audio_content = base64.b64decode(audio_content_base64)

        # Convert and save to MP3
        with tempfile.NamedTemporaryFile(suffix=".m4a", delete=False) as temp_audio:
            temp_audio.write(audio_content)
            temp_audio.close()

            audio_clip = AudioFileClip(temp_audio.name)
            output_file = f"converted_audio.mp3"
            audio_clip.write_audiofile(output_file)
            audio_clip.close()

            # Send completion message
            await websocket.send(f"Conversion done: {output_file}")
    
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        await websocket.send(f"ERROR:{str(e)}")
    
    finally:
        await websocket.close()

start_server = websockets.serve(convert_audio, "localhost", 8888)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
