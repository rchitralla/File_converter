import streamlit as st
import websocket
import base64

def main():
    st.title("Audio File to MP3 Converter with WebSocket Integration")
    st.write("Upload an audio file and convert it to MP3.")

    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "ogg", "flac", "aac", "m4a", "wma", "amr", "mka"])

    if uploaded_file is not None:
        st.write(f"Uploaded file: {uploaded_file.name}")

        if st.button("Convert to MP3"):
            websocket_url = "ws://localhost:8888/convert"
            ws = websocket_client.WebSocket()
            ws.connect(websocket_url)

            with uploaded_file as f:
                file_content = f.read()
                base64_content = base64.b64encode(file_content).decode('utf-8')
                ws.send(base64_content)

                result = ws.recv()
                st.write(f"Conversion result: {result}")

            ws.close()
            st.success("File converted successfully!")

if __name__ == "__main__":
    main()
