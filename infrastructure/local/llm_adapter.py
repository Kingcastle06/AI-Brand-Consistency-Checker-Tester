from typing import Optional
from PIL import Image

from google import genai
from google.genai import types

def generate_completion(
    prompt: str, 
    system_instruction: Optional[str] = None,
    image_path: Optional[str] = None
) -> str:
    """
    Generate a text completion using the Google GenAI SDK.
    Supports multimodal inputs by passing an optional image file path.
    This wrapper hides all vendor-specific code from the inner package.
    """
    # Initialize the client. It will automatically use the GEMINI_API_KEY environment variable.
    client = genai.Client()
    
    config = types.GenerateContentConfig()
    if system_instruction:
        config.system_instruction = system_instruction
        
    # Build out the contents list. For text-only, it stays a single string block.
    # For multimodal items, it bundles both the PIL image object and the prompt.
    contents_payload = [prompt]
    
    if image_path:
        # Load the raw graphic asset using PIL
        img = Image.open(image_path)
        contents_payload.insert(0, img)
        
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents_payload,
        config=config,
    )
    
    return response.text