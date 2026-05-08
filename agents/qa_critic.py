"""
Quality Assurance Agent ("The Critic")

This agent evaluates the generated cartoon. It uses a powerful 
multimodal VLM to perform two checks:
1. Style Compliance: Does the image match the requested cartoon style?
2. Identity Match: Does the cartoon character still look like the person 
   in the original photo?
Based on its assessment, it either approves the image or provides 
constructive feedback.
"""
import ollama
import base64
import json

class QACritic:
    def __init__(self, model="llava:latest"):
        self.model = model

    def evaluate_image(self, state):
        """
        Evaluates the generated image against the original.
        
        Args:
            state (dict): The current state of the workflow.
            
        Returns:
            dict: A dictionary containing the feedback.
        """
        original_image_path = state["image_path"]
        generated_image_path = state["generated_image"]
        style_prompt = state["style_prompt"]
        
        print(f"--- Evaluating generated image: {generated_image_path} ---")

        with open(original_image_path, "rb") as f:
            original_image_b64 = base64.b64encode(f.read()).decode('utf-8')
        with open(generated_image_path, "rb") as f:
            generated_image_b64 = base64.b64encode(f.read()).decode('utf-8')

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'user',
                        'content': f'You are a Quality Assurance critic. Compare the two images. The first is the original photo, the second is a generated cartoon. Does the cartoon match the requested style "{style_prompt}"? Does the cartoon maintain the identity of the person in the original photo? Respond with a JSON object with two keys: "approved" (boolean) and "feedback" (a string with your reasoning and suggestions for improvement if not approved).',
                        'images': [original_image_b64, generated_image_b64]
                    }
                ],
                format="json"
            )
            feedback_json = json.loads(response['message']['content'])
            print(f"--- Evaluation complete. Feedback: {feedback_json} ---")
            return {"feedback": feedback_json}
        except Exception as e:
            print(f"Error during evaluation: {e}")
            return {"feedback": {"approved": False, "feedback": "Error during evaluation."}}
