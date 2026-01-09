from urllib import response
from mcp.server.fastmcp import FastMCP
import os
import uuid
from pathlib import Path
from google import genai


mcp = FastMCP("mcp-server-demo")

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

OUTPUT_DIR = Path("generated_images")
OUTPUT_DIR.mkdir(exist_ok=True)

## IMAGE GENERATOR
@mcp.tool()
def generate_image(prompt: str) -> str:
    """
    Gera uma imagem usando Gemini (SDK google.genai)
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[prompt],
        config=genai.types.GenerateContentConfig(
            response_modalities=["IMAGE"]
        ),
    )
    parts = response.candidates[0].content.parts
    for part in parts:
        if part.text is not None:
            print(part.text)
            
        elif part.inline_data is not None:
            image = part.as_image()
            output_path = OUTPUT_DIR / "generated_image.png"
            image.save(output_path)
            return str(output_path)
    return "No image generated."
    


## TOOL DO AGENTE

@mcp.tool()
def agent_image(goal : str) -> str:
    if "imagem" in goal.lower() or "image" in goal.lower():
        prompt = f"Create an image that represents the following goal: {goal}"
        image_path = generate_image(prompt)
    else:
        image_path = "No image generated as the goal does not specify an image requirement."

    return image_path


## run MCP server
if __name__ == "__main__":
    mcp.run()
