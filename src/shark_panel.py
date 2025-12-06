import json
import google.generativeai as genai
from src.utils import setup_logging, get_api_key

logger = setup_logging(__name__)

class SharkPanel:
    def __init__(self):
        self.api_key = get_api_key()
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            self.model = None
        
        self.personas = {
            "The Visionary": "Focuses on market potential, innovation, and big dreams. Loves disruption. Ignores small details.",
            "The Finance Shark": "Focuses on margins, customer acquisition costs (CAC), valuation, and profitability. Very critical of fuzzy numbers.",
            "The Skeptic": "Challenges assumptions, looks for risks, questions the team's ability to execute. Hard to impress."
        }

    def generate_feedback(self, transcript, tone_data, content_data):
        """
        Generates feedback from each shark persona based on the pitch analysis.
        """
        if not self.model:
            return self._get_mock_feedback()

        logger.info("Generating Shark Panel feedback...")
        
        # Construct context
        context = f"""
        PITCH TRANSCRIPT:
        "{transcript}"

        TONE ANALYSIS:
        - Pitch Variation: {tone_data.get('pitch_variation', 'N/A')}
        - Energy: {tone_data.get('energy_avg', 'N/A')}
        - Pace: {tone_data.get('estimated_tempo', 'N/A')}
        - Delivery Score: {tone_data.get('delivery_score', 'N/A')}
        - Detected Emotion: {tone_data.get('ai_analysis', {}).get('emotion', 'Unknown')}
        - Vocal Confidence: {tone_data.get('ai_analysis', {}).get('confidence', 'Unknown')}

        BUSINESS ANALYSIS:
        - Problem Clarity: {content_data.get('scores', {}).get('problem_clarity', 'N/A')}
        - Business Model: {content_data.get('scores', {}).get('business_model', 'N/A')}
        - Market Opportunity: {content_data.get('scores', {}).get('market_opportunity', 'N/A')}
        - Viability Score: {content_data.get('overall_viability_score', 'N/A')}
        """

        prompt = f"""
        You are a panel of investors on a show like Shark Tank.
        Based on the pitch info below, generate a response from each of the following personas:

        {json.dumps(self.personas, indent=2)}

        CONTEXT:
        {context}

        INSTRUCTIONS:
        1. Each shark should give a specific critique in their unique voice.
        2. "The Finance Shark" must reference the numbers/business model.
        3. "The Visionary" must reference the market/idea.
        4. "The Skeptic" must point out a flaw.
        5. Provide a final "Invest" or "Not Invest" or "Need Info" decision for the group.

        OUTPUT FORMAT (JSON):
        {{
            "sharks": [
                {{
                    "name": "The Visionary",
                    "feedback": "...",
                    "decision": "Invest/Not Invest"
                }},
                ...
            ],
            "final_verdict": "Invest/Not Invest/Need More Info",
            "summary_reason": "..."
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            text = response.text.replace("```json", "").replace("```", "").strip()
            feedback = json.loads(text)
            logger.info("Shark feedback generated.")
            return feedback
        except Exception as e:
            logger.error(f"Shark feedback generation failed: {e}")
            return self._get_mock_feedback()

    def _get_mock_feedback(self):
        return {
            "sharks": [
                {
                    "name": "The Visionary",
                    "feedback": "I love the energy! This could be huge if you can scale it.",
                    "decision": "Invest"
                },
                {
                    "name": "The Finance Shark",
                    "feedback": "I don't see how you make money. The margins are too thin.",
                    "decision": "Not Invest"
                },
                {
                    "name": "The Skeptic",
                    "feedback": "I've seen this before and it failed. Why are you different?",
                    "decision": "Not Invest"
                }
            ],
            "final_verdict": "Not Invest",
            "summary_reason": "Great idea but the numbers don't add up yet."
        }
