import vertexai
from vertexai.generative_models import GenerativeModel
import logging

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, project_id, location="us-central1"):
        self.project_id = project_id
        self.location = location
        self.mock_mode = False 
        try:
            vertexai.init(project=project_id, location=location)
            # User explicitly requested "gemini-2.5-flash"
            self.model = GenerativeModel("gemini-2.5-flash")
        except Exception as e:
            logger.error(f"Failed to initialize Vertex AI: {e}")
            self.model = None

    def generate_content(self, prompt):
        """Generates content using the LLM."""
        if not self.model:
            logger.error("Vertex AI model not initialized.")
            return "Error: Model not initialized."
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            return f"Error: {e}"
