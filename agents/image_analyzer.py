"""
Image Analysis Agent ("The Observer")

This agent's key task is to "see" and understand the input photo. 
It uses a Vision Language Model (VLM) to generate a detailed, 
structured text description of the person in the image, capturing 
key identity markers like hair color and style, facial expression, 
clothing, and pose.
"""
import ollama
import base64

class ImageAnalyzer:
    def __init__(self, model="llava:latest"):
        self.model = model

    def analyze_image(self, image_path: str):
        """
        Analyzes the image using a VLM and returns a structured description.
        
        Args:
            image_path (str): The path to the input image.
            
        Returns:
            str: A textual description of the image.
        """
        print(f"--- Analyzing image: {image_path} ---")
        
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'user',
                        'content': 'Describe the person in this image in detail, focusing on hair color, hairstyle, facial expression, clothing, and pose. This description will be used to generate a cartoon version of them.',
                        'images': [encoded_string]
                    }
                ]
            )
            description = response['message']['content']
            print(f"--- Image analysis complete. Description: {description} ---")
            return {"analysis": description}
        except Exception as e:
            print(f"Error during image analysis: {e}")
            return {"analysis": "Error during image analysis."}
