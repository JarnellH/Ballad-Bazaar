# Ballad-Bazaar
This repo houses Ballad Bazaar AI Hackathon Project 

To run:
Start Flask server with:
`python main.py`

Start Modal server (which does video generation and listens to Cyanite webhook events) with:
`modal serve video_gen.py`

Application is accessible at:
`http://localhost:3000`

Flask Server responsible for orchestrating video creation process:
- Creates prompts for all videos using GPT + lyrics + music analysis information
- Stitches together videos and adds effects/transitions
- Overlaying soundtrack over newly created music video

Technlogies Used:
- Huggingface text-2-video model
- Huggingface video-2-video model (for upscaling)
- Modal + FastAPI (for running GPU-heavy video generation models in the cloud)
- Flask for backend, communicating with Modal API + frontend
- GPT-4 for video generation prompt creation
- Cyanite.ai for music analysis (mood, genre, energy, etc.)
- Moviepy for editing all music video components together into single video
- HTML/CSS + JavaScript for UI
- TikTok/Instagram API for sharing generated video