# Shark Tank Pitch Analyzer 🦈

A multimodal AI pipeline that analyzes pitch videos/audio for both vocal delivery and business content, providing feedback from virtual "Shark" personas.

## Features

- **Voice & Tone Analysis**: Extracts pitch, pace, energy, and pauses to score delivery.
- **Business Content Analysis**: Transcribes speech and evaluates business logic (Problem, Solution, Market, etc.).
- **Virtual Shark Panel**: Generates personalized feedback from 3 AI personas (Visionary, Finance Shark, Skeptic).
- **Interactive UI**: Streamlit-based interface for easy uploading and visualization.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **API Key**:
    You need a Google Gemini API Key.
    - Create a `.env` file in the root directory:
      ```
      GOOGLE_API_KEY=your_api_key_here
      ```
    - OR enter it in the Streamlit sidebar.

## Usage

### Run the Web Interface
```bash
streamlit run app.py
```

### Run via CLI
```bash
python main.py path/to/your/pitch.mp4
```

## Architecture

- `src/input_handler.py`: Handles video->audio conversion.
- `src/tone_analysis.py`: Uses Librosa for signal processing.
- `src/asr_engine.py`: Uses Gemini API for transcription.
- `src/content_analysis.py`: Uses Gemini API for business scoring.
- `src/shark_panel.py`: Generates persona-based feedback.

## Testing
Run the verification script:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python tests/test_pipeline.py
```
