import librosa
import numpy as np
import google.generativeai as genai
from src.utils import setup_logging, get_api_key

logger = setup_logging(__name__)

class ToneAnalyzer:
    def __init__(self):
        self.api_key = get_api_key()
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            self.model = None

    def analyze_audio(self, audio_path):
        """
        Analyzes the audio file and returns a dictionary of vocal features.
        """
        logger.info(f"Starting tone analysis for {audio_path}")
        try:
            y, sr = librosa.load(audio_path, sr=None)
            
            # 1. Signal Processing Metrics
            pitch_avg = self._analyze_pitch(y, sr)
            pitch_std = self._analyze_pitch_variation(y, sr)
            energy_avg = self._analyze_energy(y)
            pause_ratio = self._analyze_pauses(y, sr)
            tempo = self._estimate_tempo(y, sr)
            
            features = {
                "pitch_avg": pitch_avg,
                "pitch_variation": pitch_std,
                "energy_avg": energy_avg,
                "pause_ratio": pause_ratio,
                "estimated_tempo": tempo
            }
            
            # 2. Heuristic Scoring (Calibrated)
            features["monotony_score"] = self._calculate_monotony(pitch_std)
            features["delivery_score"] = self._calculate_delivery_score(features)
            
            # 3. Human Labels
            features["labels"] = self._get_human_labels(features)
            
            # 4. AI Vibe Check (Gemini)
            features["ai_analysis"] = self._analyze_with_ai(audio_path)
            
            logger.info(f"Tone analysis complete: {features}")
            return features
        except Exception as e:
            logger.error(f"Error in tone analysis: {e}")
            return {}

    def _analyze_with_ai(self, audio_path):
        if not self.model:
            return {"emotion": "Unknown", "confidence": "Unknown", "tips": []}
        
        try:
            audio_file = genai.upload_file(path=audio_path)
            prompt = """
            Listen to this pitch audio. 
            1. Describe the speaker's emotion (e.g., Passionate, Nervous, Robotic, Confident).
            2. Rate their vocal confidence (Low/Medium/High).
            3. Give 1 specific coaching tip on their voice (e.g., "Speak louder", "Slow down", "Vary pitch").
            
            Return JSON: {"emotion": "...", "confidence": "...", "tip": "..."}
            """
            response = self.model.generate_content([prompt, audio_file])
            import json
            text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception as e:
            logger.error(f"AI Vibe Check failed: {e}")
            return {"emotion": "Unknown", "confidence": "Unknown", "tip": "Could not analyze audio vibe."}

    def _analyze_pitch(self, y, sr):
        f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
        valid_f0 = f0[~np.isnan(f0)]
        if len(valid_f0) == 0: return 0.0
        return float(np.mean(valid_f0))

    def _analyze_pitch_variation(self, y, sr):
        f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
        valid_f0 = f0[~np.isnan(f0)]
        if len(valid_f0) == 0: return 0.0
        return float(np.std(valid_f0))

    def _analyze_energy(self, y):
        rms = librosa.feature.rms(y=y)
        return float(np.mean(rms))

    def _analyze_pauses(self, y, sr):
        intervals = librosa.effects.split(y, top_db=25) # Increased threshold to ignore breathing
        non_silent_samples = sum((end - start) for start, end in intervals)
        return float((len(y) - non_silent_samples) / len(y))

    def _estimate_tempo(self, y, sr):
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
        return float(tempo[0])

    def _calculate_monotony(self, pitch_std):
        # Calibrated: < 15Hz is monotone, > 40Hz is expressive
        if pitch_std < 15: return 100
        elif pitch_std > 50: return 0
        else: return 100 - ((pitch_std - 15) / 35 * 100)

    def _calculate_delivery_score(self, features):
        # Calibrated Scoring
        score = 65 # Higher Base
        
        # Energy (Normalized roughly 0.0 to 0.1+)
        if features["energy_avg"] > 0.02: score += 10
        
        # Pause Ratio (Ideal 10-20%)
        pr = features["pause_ratio"]
        if 0.10 <= pr <= 0.25: score += 10
        elif pr > 0.40: score -= 10
        
        # Monotony
        if features["pitch_variation"] > 25: score += 10
        elif features["pitch_variation"] < 10: score -= 10
        
        # Tempo (Ideal 110-160)
        tempo = features["estimated_tempo"]
        if 110 <= tempo <= 160: score += 5
        
        return max(0, min(100, score))

    def _get_human_labels(self, features):
        labels = {}
        
        # Pitch
        std = features["pitch_variation"]
        if std < 15: labels["pitch"] = "🤖 Monotone"
        elif std < 35: labels["pitch"] = "😐 Normal"
        else: labels["pitch"] = "🎵 Expressive"
        
        # Pace
        bpm = features["estimated_tempo"]
        if bpm < 100: labels["pace"] = "🐢 Slow"
        elif bpm > 160: labels["pace"] = "🐇 Fast"
        else: labels["pace"] = "🚶 Conversational"
        
        # Pauses
        pr = features["pause_ratio"]
        if pr > 0.30: labels["pause"] = "⏸️ Frequent Pauses"
        elif pr < 0.10: labels["pause"] = "🏃 Rushed"
        else: labels["pause"] = "✅ Natural Pacing"
        
        return labels
