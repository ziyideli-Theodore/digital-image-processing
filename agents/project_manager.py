"""
Project Manager Agent (Coordinator)

This agent is the user-facing part of the system. 
It receives the input photo and the desired cartoon style,
initiates the workflow, and assigns tasks to the appropriate experts.
"""

class ProjectManager:
    def __init__(self):
        pass

    def start_workflow(self, image_path: str, style_prompt: str):
        """
        Starts the cartoonization workflow.
        
        Args:
            image_path (str): The path to the input image.
            style_prompt (str): The user's desired cartoon style.
            
        Returns:
            dict: A dictionary containing the initial state for the workflow.
        """
        print(f"--- Starting workflow for image: {image_path} with style: {style_prompt} ---")
        return {
            "image_path": image_path,
            "style_prompt": style_prompt,
            "analysis": None,
            "generated_image": None,
            "feedback": None,
        }
