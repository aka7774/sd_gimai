import os
import pathlib
import json

from scripts import project

default_settings = {
    'input_dir': project.default_input_dir(),
    'voice_ext': 'wav',
    'image_ext': 'png',
    'moegoe_path': os.path.join('moegoe', 'moegoe.exe'),
    'moegoe_model_dir': os.path.join('moe-tts', 'saved_model'),
    'moegoe_dr': '1.25',
    'moegoe_nr': '0.600',
    'moegoe_nb': '0.80',
    'ffmpeg_path': os.path.join('ffmpeg', 'bin', 'ffmpeg.exe'),
    'build_dir': project.default_build_dir(),
    }

def get_config_path():
    p = pathlib.Path(__file__).parts[-4:-2]
    return os.path.join(p[0], p[1], 'json', 'config.json')

def load_settings():
    filepath = get_config_path()
    settings = default_settings
    if os.path.exists(filepath):
        with open(filepath) as f:
            settings.update(json.load(f))
    return settings

def save_settings(*input_settings):
    filepath = get_config_path()
    data = {}
    if os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(f)
    i = 0
    for k in default_settings.keys():
        data.update({k: input_settings[i]})
        i += 1
    with open(filepath, "w") as f:
        json.dump(data, f)
    return json.dumps(data)
