import google.generativeai as genai
import json
from config import Config

# Configure the API key
genai.configure(api_key=Config.GEMINI_API_KEY)

class GeminiClient:
    def __init__(self):
        # We explicitly use the free-tier model specified in config
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def plan_agents(self, instruction: str) -> list[dict]:
        """Analyzes user instruction and designs specifications for specialized agents."""
        prompt = f"""
        You are the Master AI Agent Architect. The user wants to build specialized AI agents.
        Analyze this request: "{instruction}"
        
        Determine what specialized agents are needed. For each, create a JSON specification.
        Respond ONLY with a valid JSON array of objects. Do not include markdown formatting like ```json.
        Each object must have these exact keys: name, domain, purpose, capabilities (list of strings), inputs (list), outputs (list), tools (list).
        """
        response = self.model.generate_content(prompt)
        try:
            cleaned = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)
        except Exception as e:
            raise ValueError(f"Failed to parse Gemini response into specifications. {str(e)}")

    def generate_agent_code(self, spec_json: str) -> str:
        """Generates the actual Python code for the specialized agent based on its spec."""
        prompt = f"""
        You are an expert Python developer. Write the complete, runnable Python code for this specialized AI agent based on this specification:
        {spec_json}
        
        Write a single, well-structured Python script (main.py) that acts as the entry point for this agent.
        Include standard libraries, class definitions, and mock functions for its capabilities if external APIs aren't provided.
        Return ONLY the raw Python code. No markdown formatting, no explanations.
        """
        response = self.model.generate_content(prompt)
        return response.text.replace("```python", "").replace("```", "").strip()