from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from modal import Image, Stub, asgi_app, NetworkFileSystem
import pprint

web_app = FastAPI()
volume = NetworkFileSystem.new()
stub = Stub("my-app")
image = Image.debian_slim().run_commands("pip install torch --extra-index-url https://download.pytorch.org/whl/cu117").apt_install("libgl-dev", "libglib2.0-0").pip_install("boto3", "torch", "diffusers", "transformers", "accelerate", "opencv-python")

@web_app.post("/foo")
async def foo(request: Request):
    body = await request.json()
    return body

@web_app.post("/cyanite_webhook")
async def cyanite_webhook(request: Request):
    # My cyanite secret: 58c6a742fc5b7cd8312c700fb06c3a0566ebe
    # Access Token:
    # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiSW50ZWdyYXRpb25BY2Nlc3NUb2tlbiIsInZlcnNpb24iOiIxLjAiLCJpbnRlZ3JhdGlvbklkIjo2MjYsInVzZXJJZCI6NTAxNjIsImFjY2Vzc1Rva2VuU2VjcmV0IjoiM2JkZDc1NzRhOGIwZTYyZGJkN2ViY2NlMmY0ZWMzZDFlY2U0MGJkNWE3MThhOGI4YjRkOTE1N2Q4N2MwOGJhYiIsImlhdCI6MTY4OTQ5Mjg2MX0.QpHTrNowFAuSgS0p8PfcrlBF8-kW37CyrOCEkncCwQ8
    body = await request.json()

    pprint.pprint(body)
    return HTMLResponse("<h1>Analyzing some music</h1>")


@web_app.get("/bar")
async def bar(arg="world"):
    return HTMLResponse(f"<h1>Hello Fast {arg}!</h1>")

@web_app.get("/vid")
async def vid(prompt="Darth Vader is surfing on waves", name="vader"):
    import torch
    from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
    from diffusers.utils import export_to_video

    pipe = DiffusionPipeline.from_pretrained("cerspense/zeroscope_v2_576w", torch_dtype=torch.float16)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe.enable_model_cpu_offload()
    pipe.enable_vae_slicing()
    # pipe.unet.enable_forward_chunking(chunk_size=1, dim=1) # disable if enough memory as this slows down significantly

    # height = 320, width = 576
    video_frames = pipe(prompt, num_inference_steps=40, height=568, width=320, num_frames=36).frames
    video_path = export_to_video(video_frames, output_video_path=f"/home/{name}.mp4")
    # file_path = "path_to_your_file/" + file_name
    file_like_object = open(video_path, mode="rb")
    response = StreamingResponse(file_like_object, media_type="video/mp4")
    response.headers["Content-Disposition"] = f'attachment; filename={name}.mp4'
    
    return response

@stub.function(
    gpu="A100",
    image=image,
    network_file_systems={"/home": volume},
)
@asgi_app()
def fastapi_app():
    return web_app


# For testing purposes:

# @stub.function(
#     gpu="A100",
#     image=(
#         modal.Image.debian_slim()
#         .run_commands(
#             "pip install torch --extra-index-url https://download.pytorch.org/whl/cu117"
#         )
#         .apt_install("libgl-dev", "libglib2.0-0")
#         .pip_install("torch", "diffusers", "transformers", "accelerate", "opencv-python")
#     ),
#     network_file_systems={"/home": volume},
# )
# async def run_vid_gen():
#     import torch
#     from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
#     from diffusers.utils import export_to_video

#     pipe = DiffusionPipeline.from_pretrained("cerspense/zeroscope_v2_576w", torch_dtype=torch.float16)
#     pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
#     pipe.enable_model_cpu_offload()
#     pipe.enable_vae_slicing()
#     # pipe.unet.enable_forward_chunking(chunk_size=1, dim=1) # disable if enough memory as this slows down significantly

#     prompt = "Darth Vader is surfing on waves"
#     video_frames = pipe(prompt, num_inference_steps=40, height=320, width=576, num_frames=36).frames
#     video_path = export_to_video(video_frames, output_video_path="/home/vader.mp4")


#     return video_path
