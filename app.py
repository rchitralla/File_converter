import streamlit as st
import websocket
from moviepy.editor import AudioFileClip
import os

def convert_audio_to_mp3(audio_file, output_file, progress_bar):
    audio_clip = AudioFileClip(audio_file.name)
    total_frames = int(audio_clip.fps * audio_clip.duration)
    audio_clip.write_audiofile(output_file, progress_bar=progress_bar)
    audio_clip.close()

def main():
    st.title("Audio File to MP3 Converter with WebSocket Integration")
    st.write("Upload an audio file and convert it to MP3.")

    # Initialize session state
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    if 'conversion_done' not in st.session_state:
        st.session_state.conversion_done = False

    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "ogg", "flac", "aac", "m4a", "wma", "amr", "mka"])

    if uploaded_file is not None:
        st.write(f"Uploaded file: {uploaded_file.name}")

        # Display file details
        file_details = {"Filename": uploaded_file.name, "Filesize": uploaded_file.size}
        st.write(file_details)
        
        # Button to start conversion
        if st.button("Convert to MP3") and not st.session_state.conversion_done:
            st.session_state.conversion_done = True  # Prevent multiple conversions
            
            # Initialize WebSocket connection
            websocket_url = "ws://localhost:8888/convert"  # Replace with your WebSocket server URL
            ws = websocket.WebSocket()
            ws.connect(websocket_url)
            
            # Start sending file content
            with uploaded_file as f:
                file_content = f.read()
                ws.send(file_content)
            
            # Monitor conversion progress
            progress_text = st.empty()
            progress_bar = st.progress(st.session_state.progress)

            while True:
                result = ws.recv()
                if result.startswith("PROGRESS"):
                    progress = float(result.split(":")[1])
                    st.session_state.progress = progress
                    progress_bar.progress(progress)
                    progress_text.text(f"Conversion progress: {progress}%")
                elif result == "DONE":
                    ws.close()
                    st.success("File converted successfully!")
                    st.session_state.progress = 0
                    st.session_state.conversion_done = False
                    break

    else:
        st.write("No file uploaded yet.")

if __name__ == "__main__":
    main()
