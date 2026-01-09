from mcp.server.fastmcp import FastMCP
from openai import OpenAI
import base64
import uuid
from pathlib import Path

mcp = FastMCP("mcp-server-demo")
client = OpenAI()

OUTPUT_DIR = Path("generated_images")
OUTPUT_DIR.mkdir(exist_ok=True)

## IMAGE GENERATOR

@mcp.tool()
def generate_image(prompt: str) -> str:
    
    """ 
    Generates an image based on the provided text prompt 
    and saves it to disk.

    Returns the file path of the saved image.
    """


    result = client.images.generate(
        model = "gpt-image-1",
        prompt = prompt,
        size = "1024x1024",
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    filename = OUTPUT_DIR / f"{uuid.uuid4()}.png"
    with open(filename, "wb") as f:
        f.write(image_bytes)

    return str(filename)

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