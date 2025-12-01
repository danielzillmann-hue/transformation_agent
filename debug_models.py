import vertexai
from vertexai.generative_models import GenerativeModel
import logging

def list_models(project_id, location="us-central1"):
    try:
        vertexai.init(project=project_id, location=location)
        # There isn't a direct "list_models" in GenerativeModel, but we can try to instantiate a few common ones
        # or use the Model Garden API if available, but let's just try to instantiate and print success/fail
        models_to_try = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro", "text-bison"]
        
        print(f"Checking models in project {project_id}, location {location}...")
        for model_name in models_to_try:
            try:
                model = GenerativeModel(model_name)
                # Just trying to instantiate might not trigger the API call until generate is called
                # So let's try a simple generation
                response = model.generate_content("Hello")
                print(f"SUCCESS: {model_name} is available.")
            except Exception as e:
                print(f"FAILED: {model_name} - {e}")
                
    except Exception as e:
        print(f"Failed to init Vertex AI: {e}")

if __name__ == "__main__":
    print("--- Checking us-central1 ---")
    list_models("gcp-sandpit-intelia", "us-central1")
    print("\n--- Checking australia-southeast1 (Sydney) ---")
    list_models("gcp-sandpit-intelia", "australia-southeast1")
    print("\n--- Checking australia-southeast2 (Melbourne) ---")
    list_models("gcp-sandpit-intelia", "australia-southeast2")
