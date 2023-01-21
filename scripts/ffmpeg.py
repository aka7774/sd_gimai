import os
import shutil
import pathlib
import subprocess
import tqdm

from scripts import project, utils

def generate_all(input_dir, voice_ext, image_ext, ffmpeg_path):
    rs = project.get_list(input_dir, voice_ext, image_ext)
    for r in tqdm.tqdm(rs):
        if r['voice']:
            generate(r['voice'], ffmpeg_path)
    return 'generated.'

def generate(voice_path, ffmpeg_path):
    save_path = os.path.splitext(voice_path)[0]+'.mp4'
    cmd = f'{ffmpeg_path} -y -i "{voice_path}" -c:a aac -b:a 128k -f mp4 "{save_path}"'
    p = subprocess.run(cmd, text=True, shell=True)
    print(cmd)

    print(f"generated {save_path}")

    return save_path
