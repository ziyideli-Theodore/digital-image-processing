"""
Art Director Agent ("The Generator")

This is the core technical artist. It receives the text description from 
the analysis agent and the original image as a reference. Its goal is to 
generate the cartoon image using a powerful combination of modern diffusion 
techniques.
"""
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
from diffusers.utils import load_image
import torch
import cv2
from PIL import Image
import numpy as np
from controlnet_aux import OpenposeDetector

class ArtDirector:
    def __init__(self, model_dir="models"):
        base_model_path = f"{model_dir}/classic-anim-diffusion"
        controlnet_path = f"{model_dir}/control_v11p_sd15_openpose"
        openpose_path = f"{model_dir}/ControlNet"
        ip_adapter_path = f"{model_dir}/IP-Adapter"

        # Load the OpenPose detector from local files
        self.openpose = OpenposeDetector.from_pretrained(openpose_path)

        # Load ControlNet from local files
        controlnet = ControlNetModel.from_pretrained(controlnet_path, torch_dtype=torch.float16)
        
        # Load the base Stable Diffusion pipeline from local files
        self.pipeline = StableDiffusionControlNetPipeline.from_pretrained(
            base_model_path, controlnet=controlnet, torch_dtype=torch.float16
        )
        self.pipeline.scheduler = UniPCMultistepScheduler.from_config(self.pipeline.scheduler.config)
        self.pipeline.enable_model_cpu_offload()
        
        # Define path for IP-Adapter for later use
        self.ip_adapter_path = ip_adapter_path

    def generate_cartoon(self, state):
        """
        Generates a cartoon image based on the analysis and original image.
        
        Args:
            state (dict): The current state of the workflow.
            
        Returns:
            dict: A dictionary containing the path to the generated image.
        """
        image_path = state["image_path"]
        analysis = state["analysis"]
        style_prompt = state["style_prompt"]
        
        print(f"--- Generating cartoon for: {image_path} ---")

        # Prepare the prompt
        prompt = f"{analysis}, in the style of {style_prompt}"
        negative_prompt = "monochrome, lowres, bad anatomy, worst quality, low quality"

        # Load and process the input image for OpenPose
        original_image = load_image(image_path)
        pose_image = self.openpose(original_image)
        
        # Load the IP-Adapter from local files
        self.pipeline.load_ip_adapter(self.ip_adapter_path, subfolder="models", weight_name="ip-adapter_sd15.bin")
        self.pipeline.set_ip_adapter_scale(0.6)

        # Generate the image
        generator = torch.manual_seed(0)
        generated_image = self.pipeline(
            prompt,
            num_inference_steps=30,
            generator=generator,
            image=pose_image,
            ip_adapter_image=original_image,
            negative_prompt=negative_prompt,
        ).images[0]

        # Save the generated image
        output_path = "generated_cartoon.png"
        generated_image.save(output_path)
        print(f"--- Cartoon generated and saved to {output_path} ---")
        
        return {"generated_image": output_path}
