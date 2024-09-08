import asyncio
import os
import logging
from moviepy.editor import VideoFileClip

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def get_video_duration(input_file):
    logger.info(f"Getting duration of video: {input_file}")
    clip = VideoFileClip(input_file)
    duration = clip.duration
    clip.close()
    logger.info(f"Video duration: {duration:.2f} seconds")
    return duration

async def run_command(command):
    logger.info(f"Running command: {' '.join(command)}")
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        logger.error(f"Command failed: {' '.join(command)}")
        logger.error(f"Error output: {stderr.decode()}")
        raise Exception(f"Command failed: {' '.join(command)}")
    logger.info(f"Command completed successfully: {' '.join(command)}")

async def create_gif_preview(input_file, output_file, clip_duration=1, num_clips=4):
    logger.info(f"Starting GIF preview creation for: {input_file}")
    
    total_duration = await get_video_duration(input_file)
    
    interval = (total_duration - clip_duration) / (num_clips - 1)
    logger.info(f"Interval between clips: {interval:.2f} seconds")
    
    select_filter = '+'.join([f"between(t,{i*interval},{i*interval+clip_duration})" for i in range(num_clips)])
    ffmpeg_command = [
        "ffmpeg", "-i", input_file,
        "-filter_complex",
        f"select='{select_filter}',"
        "setpts=N/FRAME_RATE/TB,fps=15,scale=320:-1:flags=lanczos,split [a][b];"
        "[a] palettegen=stats_mode=diff [p];"
        "[b][p] paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
        "-loop", "0",
        output_file
    ]
    
    await run_command(ffmpeg_command)
    
    logger.info(f"GIF preview creation completed: {output_file}")
