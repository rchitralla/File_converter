import streamlit as st
from moviepy.editor import AudioFileClip

def convert_audio_to_mp3(audio_file, output_file):
    # Load the audio file clip
    audio_clip = AudioFileClip(audio_file)
    
    # Calculate the total number of frames for the progress bar
    total_frames = int(audio_clip.fps * audio_clip.duration)
    
    # Initialize a progress bar with the total number of frames
    progress_bar = st.progress(0)
    
    # Write the audio clip to an MP3 file
    audio_clip.write_audiofile(output_file, progress_bar=progress_bar)
    
    # Close the audio clip
    audio_clip.close()

def main():
    st.write("Starting the app...")

    st.title("Audio File to MP3 Converter")
    st.write("Upload an audio file and convert it to MP3.")

    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "ogg", "flac", "aac", "m4a", "wma", "amr", "mka"])

    if uploaded_file is not None:
        st.write(f"Uploaded file: {uploaded_file.name}")

        # Display file details
        file_details = {"Filename": uploaded_file.name, "Filesize": uploaded_file.size}
        st.write(file_details)
        
        # Convert and save to MP3
        output_file = f"converted_{uploaded_file.name.split('.')[0]}.mp3"
        st.write(f"Converting to MP3: {output_file}")
        convert_audio_to_mp3(uploaded_file, output_file)
        
        # Display success message with download link
        st.success(f"File converted successfully! [Download MP3 file]({output_file})")
    else:
        st.write("No file uploaded yet.")

    st.write("App finished.")

        
        # Convert and save to MP3
        output_file = f"converted_{uploaded_file.name.split('.')[0]}.mp3"
        convert_audio_to_mp3(uploaded_file, output_file)
        
        # Display success message with download link
        st.success(f"File converted successfully! [Download MP3 file]({output_file})")
    
if __name__ == "__main__":
    main()
