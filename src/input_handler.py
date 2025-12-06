import os
from moviepy import VideoFileClip, AudioFileClip
from src.utils import setup_logging

logger = setup_logging(__name__)

class InputHandler:
    def __init__(self, output_dir="data/processed"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def process_input(self, input_path):
        """
        Processes the input file (video or audio) and returns the path to the cleaned audio file.
        """
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        ext = ext.lower()

        output_audio_path = os.path.join(self.output_dir, f"{name}.wav")

        try:
            if ext in ['.mp4', '.mov', '.avi', '.mkv']:
                logger.info(f"Processing video file: {input_path}")
                self._extract_audio_from_video(input_path, output_audio_path)
            elif ext in ['.wav', '.mp3', '.m4a']:
                logger.info(f"Processing audio file: {input_path}")
                self._convert_audio(input_path, output_audio_path)
            else:
                raise ValueError(f"Unsupported file format: {ext}")
            
            return output_audio_path
        except Exception as e:
            logger.error(f"Error processing input: {e}")
            raise

    def _extract_audio_from_video(self, video_path, output_path):
        """
        Extracts audio from video using moviepy.
        """
        try:
            video = VideoFileClip(video_path)
            # Write audio as wav, 16kHz, mono for best compatibility with ASR/Analysis
            video.audio.write_audiofile(output_path, fps=16000, nbytes=2, codec='pcm_s16le', ffmpeg_params=["-ac", "1"], logger=None)
            logger.info(f"Audio extracted to {output_path}")
        except Exception as e:
            logger.error(f"Failed to extract audio: {e}")
            raise

    def _convert_audio(self, input_path, output_path):
        """
        Converts/Normalizes input audio to standard wav format.
        """
        try:
            # We can use moviepy's AudioFileClip for audio conversion too, or ffmpeg directly.
            # Using AudioFileClip for consistency.
            audio = AudioFileClip(input_path)
            # Normalize audio using ffmpeg-python or just rely on moviepy's default which is usually okay, 
            # but let's add a specific normalization filter if possible. 
            # For simplicity and robustness without extra deps, we will just ensure it's standard 16-bit PCM.
            # To truly normalize, we'd need pydub or complex ffmpeg filters. 
            # Let's stick to standard conversion but ensure high quality.
            audio.write_audiofile(output_path, fps=16000, nbytes=2, codec='pcm_s16le', ffmpeg_params=["-ac", "1", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11"], logger=None)
            logger.info(f"Audio converted to {output_path}")
        except Exception as e:
            logger.error(f"Failed to convert audio: {e}")
            raise
