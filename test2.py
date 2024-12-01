from diffusers import StableDiffusionPipeline
import torch

# Load the model
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float32)
pipe = pipe.to("cuda")

# Generate image
prompt = "A futuristic cityscape at sunset"
image = pipe(prompt).images[0]

# Save or display the image
image.save("output.png")
