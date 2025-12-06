import os
import argparse
from src.input_handler import InputHandler
from src.tone_analysis import ToneAnalyzer
from src.asr_engine import ASREngine
from src.content_analysis import ContentAnalyzer
from src.shark_panel import SharkPanel
from src.utils import setup_logging

logger = setup_logging(__name__)

def analyze_pitch(input_path):
    """
    Main orchestration function.
    """
    results = {}
    
    # 1. Input Processing
    logger.info("Phase 1: Input Processing")
    input_handler = InputHandler()
    audio_path = input_handler.process_input(input_path)
    results['audio_path'] = audio_path
    
    # 2. Voice & Tone Analysis
    logger.info("Phase 2: Tone Analysis")
    tone_analyzer = ToneAnalyzer()
    tone_metrics = tone_analyzer.analyze_audio(audio_path)
    results['tone_metrics'] = tone_metrics
    
    # 3. ASR (Transcription)
    logger.info("Phase 3: Transcription")
    asr_engine = ASREngine()
    transcript = asr_engine.transcribe(audio_path)
    results['transcript'] = transcript
    
    # 4. Content Analysis
    logger.info("Phase 4: Content Analysis")
    content_analyzer = ContentAnalyzer()
    content_metrics = content_analyzer.analyze_content(transcript)
    results['content_metrics'] = content_metrics
    
    # 5. Shark Panel Feedback
    logger.info("Phase 5: Shark Panel")
    shark_panel = SharkPanel()
    shark_feedback = shark_panel.generate_feedback(transcript, tone_metrics, content_metrics)
    results['shark_feedback'] = shark_feedback
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shark Tank Pitch Analyzer")
    parser.add_argument("input_file", help="Path to the video or audio file")
    args = parser.parse_args()
    
    if os.path.exists(args.input_file):
        results = analyze_pitch(args.input_file)
        print("\n--- ANALYSIS COMPLETE ---\n")
        print(results)
    else:
        print("File not found.")
