import json
import google.generativeai as genai
from src.utils import setup_logging, get_api_key

logger = setup_logging(__name__)

class ContentAnalyzer:
    def __init__(self):
        self.api_key = get_api_key()
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            self.model = None

    def analyze_content(self, transcript):
        """
        Analyzes the transcript for business content and returns scores.
        """
        if not self.model:
            return self._get_mock_analysis()

        logger.info("Starting content analysis...")
        
        prompt = f"""
        You are an expert Venture Capitalist and Business Analyst. 
        Analyze the following pitch transcript and provide a structured evaluation.

        TRANSCRIPT:
        "{transcript}"

        EVALUATION CRITERIA:
        1. Problem Clarity (0-100): How clearly is the problem defined?
        2. Product Differentiation (0-100): How unique is the solution?
        3. Business Model (0-100): Is the revenue model clear and viable?
        4. Market Opportunity (0-100): Is the market size and potential clear?
        5. Competition Awareness (0-100): Does the founder understand the landscape?

        STRUCTURE DETECTION:
        Identify if the following sections are present: Hook, Problem, Solution, Ask.

        OUTPUT FORMAT:
        Return ONLY a valid JSON object with the following structure:
        {{
            "scores": {{
                "problem_clarity": int,
                "product_differentiation": int,
                "business_model": int,
                "market_opportunity": int,
                "competition_awareness": int
            }},
            "structure": {{
                "hook": bool,
                "problem": bool,
                "solution": bool,
                "ask": bool
            }},
            "feedback": {{
                "strengths": ["point 1", "point 2"],
                "weaknesses": ["point 1", "point 2"]
            }},
            "overall_viability_score": int
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            # Clean up json if needed (sometimes models add markdown)
            text = response.text.replace("```json", "").replace("```", "").strip()
            analysis = json.loads(text)
            
            # --- NEW: Filler Word Analysis ---
            fillers = ['um', 'uh', 'like', 'you know', 'basically', 'actually', 'sort of']
            filler_count = 0
            found_fillers = {}
            lower_transcript = transcript.lower()
            
            for word in fillers:
                count = lower_transcript.count(word)
                if count > 0:
                    found_fillers[word] = count
                    filler_count += count
            
            analysis['filler_analysis'] = {
                'total_count': filler_count,
                'breakdown': found_fillers,
                'cleanliness_score': max(0, 100 - (filler_count * 2)) # Simple penalty
            }
            # ---------------------------------

            logger.info("Content analysis complete.")
            return analysis
        except Exception as e:
            logger.error(f"Content analysis failed: {e}")
            return self._get_mock_analysis()

    def _get_mock_analysis(self):
        return {
            "scores": {
                "problem_clarity": 75,
                "product_differentiation": 60,
                "business_model": 50,
                "market_opportunity": 80,
                "competition_awareness": 40
            },
            "structure": {
                "hook": True,
                "problem": True,
                "solution": True,
                "ask": False
            },
            "feedback": {
                "strengths": ["Good energy", "Clear market size"],
                "weaknesses": ["No clear ask", "Vague revenue model"]
            },
            "overall_viability_score": 65
        }
