import streamlit as st
import requests

def main():
    st.title("Audio File to MP3 Converter with WebSocket Integration")
    st.write("Upload an audio file and convert it to MP3.")

    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "ogg", "flac", "aac", "m4a", "wma", "amr", "mka"])

    if uploaded_file is not None:
        st.write(f"Uploaded file: {uploaded_file.name}")

        # Display file details
        file_details = {"Filename": uploaded_file.name, "Filesize": uploaded_file.size}
        st.write(file_details)
        
        # Button to start conversion
        if st.button("Convert to MP3"):
            # Send file to WebSocket server for conversion
            websocket_url = "ws://localhost:8888/convert"  # Replace with your WebSocket server URL
            ws = websocket.WebSocket()
            ws.connect(websocket_url)
            
            # Start sending file content
            with uploaded_file as f:
                file_content = f.read()
                ws.send(file_content)
            
            # Monitor conversion progress
            progress_text = st.empty()
            progress_bar = st.progress(0)

            while True:
                result = ws.recv()
                if result.startswith("PROGRESS"):
                    progress = float(result.split(":")[1])
                    progress_bar.progress(progress)
                    progress_text.text(f"Conversion progress: {progress}%")
                elif result == "DONE":
                    ws.close()
                    st.success("File converted successfully!")
                    break

    else:
        st.write("No file uploaded yet.")

if __name__ == "__main__":
    main()
