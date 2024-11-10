import yt_dlp as youtube_dl
import gradio as gr
import tempfile
import shutil
import os

# Function to download audio from YouTube
def download_audio_youtube(video_url):
    try:
        # Create a temporary directory to store the audio file
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': temp_dir + '/%(title)s.%(ext)s',
                'max_filesize': 25 * 1024 * 1024,  # 25 MB in bytes
                'keepvideo': False,
                'noplaylist': True,
                'noprogress': False,
                'postprocessor_args': [
                    '-acodec', 'libmp3lame',
                    '-b:a', '192k',
                ],
                'prefer_ffmpeg': True,
            }
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                # Extract information without downloading first
                info_dict = ydl.extract_info(video_url, download=False)
                video_title = info_dict.get('title', 'Unknown Title')  # Get video title
                
                # Now proceed to download the video
                ydl.download([video_url])
                
                # Get the downloaded file path
                audio_file_path = f"{temp_dir}/{video_title}.mp3"
                
                # Move the audio file to a more accessible location for downloading
                output_file_path = f"./{video_title}.mp3"
                shutil.move(audio_file_path, output_file_path)
                
                # Return the download button for the audio file
                return gr.File(label="Download Now", value=output_file_path)
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Create Gradio interface
iface = gr.Interface(
    fn=download_audio_youtube,
    inputs=gr.Textbox(label="YouTube URL"),
    outputs=gr.File(label="Download Audio"),
    title="YouTube Audio Downloader",
    description="Enter a YouTube URL to extract the audio. Limited to 25 MB per download. You can download the extracted audio after it is ready."
)

iface.launch(server_name="0.0.0.0", server_port=3000)