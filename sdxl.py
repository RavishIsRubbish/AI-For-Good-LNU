import torch
from auto1111sdk import StableDiffusionXLPipeline

cuda_available = torch.cuda.is_available()
print("Is GPU available: " + str(cuda_available))
if not cuda_available:
    print("Program cannot run without CUDA enabled GPU")
    quit(-1)

print("loading sdxl turbo model...")
pipe = StableDiffusionXLPipeline("sd_xl_turbo_1.0_fp16.safetensors", "--skip-torch-cuda-test --medvram")
pipe.set_vae("sdxl.vae.safetensors")
print("sdxl turbo model loading complete...")


def gen_image(prompt, negative_prompt):
    image = (pipe.generate_txt2img(
        prompt=prompt, negative_prompt=negative_prompt,
        width=512, height=512,
        steps=2, cfg_scale=1.3, num_images=1))[0]
    return image
