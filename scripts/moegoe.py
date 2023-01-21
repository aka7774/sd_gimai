import os
import shutil
import pathlib
import json
import glob
import subprocess
import tqdm

from scripts import project, utils

def generate_sample(message, id, input_dir, voice_ext, image_ext, model_dir, moegoe_path, moegoe_dr, moegoe_nr, moegoe_nb, moegoe_ja):
    rs = get_sample_list(message, id, model_dir, voice_ext, image_ext)
    return generate_all_inner(rs, input_dir, model_dir, moegoe_path, moegoe_dr, moegoe_nr, moegoe_nb, moegoe_ja)

def generate_all(input_dir, voice_ext, image_ext, model_dir, moegoe_path, moegoe_dr, moegoe_nr, moegoe_nb, moegoe_ja):
    rs = project.get_list(input_dir, voice_ext, image_ext)
    return generate_all_inner(rs, input_dir, model_dir, moegoe_path, moegoe_dr, moegoe_nr, moegoe_nb, moegoe_ja)

def generate_all_inner(rs, input_dir, model_dir, moegoe_path, moegoe_dr, moegoe_nr, moegoe_nb, moegoe_ja):
    for r in tqdm.tqdm(rs):
        # model_id:speaker_id:speaker_name
        n = r['name'].split(':')
        if len(n) < 3:
            continue
        generate(r['title'], r['text'], n[0], n[1], input_dir, model_dir, moegoe_path, moegoe_dr, moegoe_nr, moegoe_nb, moegoe_ja)
    return 'generated.'

def generate(title, text, model_id, speaker_id, input_dir, model_dir, moegoe_path, moegoe_dr, moegoe_nr, moegoe_nb, moegoe_ja):
    if not os.path.exists(input_dir):
        raise ValueError(f"input_dir not found: {input_dir}")
    if not os.path.exists(model_dir):
        raise ValueError(f"model_dir not found: {model_dir}")
    if not os.path.exists(moegoe_path):
        raise ValueError(f"MoeGoe not found: {moegoe_path}")

    model_path = os.path.abspath(os.path.join(model_dir, model_id, 'model.pth'))
    config_path = os.path.abspath(os.path.join(model_dir, model_id, 'config.json'))
    save_path = os.path.abspath(os.path.join(input_dir, f"{title}.wav"))
    cmd = f"{moegoe_path} --escape"
    p = subprocess.Popen(cmd, text=True, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    inputs = '\n'.join([
        #Path of a VITS model: path\to\model.pth
        model_path.replace(os.sep, '/'),
        #Path of a config file: path\to\config.json
        config_path.replace(os.sep, '/'),
        #TTS or VC? (t/v):t
        't',
        #Text to read:
        f"[LENGTH={moegoe_dr}][NOISE={moegoe_nr}][NOISEW={moegoe_nb}]{moegoe_ja}{text}{moegoe_ja}",
        #Speaker ID:
        speaker_id,
        #Path to save: path\to\demo.wav
        save_path.replace(os.sep, '/'),
        #Continue? (y/n):
        'n',
    ])
    print(inputs)
    o, e = p.communicate(input=inputs)
    if e:
        raise ValueError(f"MoeGoe Error: {e}")

    print(f"generated {save_path}")

    return save_path

def get_sample_list(message, id, model_dir, voice_ext, image_ext):
    rs = []
    info_json = os.path.join(model_dir, "info.json")
    if not os.path.exists(info_json):
        return rs
    with open(info_json, "r", encoding="utf-8") as f:
        models_info = json.load(f)
    for i, m in models_info.items():
        if i != id:
            continue
        m['config_path'] = os.path.join(model_dir, i, 'config.json')
        hps = utils.get_hparams_from_file(m['config_path'])
        for sid, name in enumerate(hps.speakers):
            r = {}
            r['scene'] = str(i).zfill(3)
            r['line'] = 'm'+str(sid).zfill(3)
            r['title'] = r['scene']+r['line']
            r['name'] = f"{i}:{sid}:{name}"
            r['text'] = message
            r['voice'] = ''
            r['image'] = ''

            rs.append(r)
    return rs

def get_list(model_dir):
    rs = []
    info_json = os.path.join(model_dir, "info.json")
    if not os.path.exists(info_json):
        return rs
    with open(info_json, "r", encoding="utf-8") as f:
        models_info = json.load(f)
    for i, m in models_info.items():
        m['model_id'] = i
        m['cover_path'] = f"{model_dir}/{i}/{m['cover']}" if m['cover'] else None
        m['config_path'] = os.path.join(model_dir, i, 'config.json')
        m['model_path'] = os.path.join(model_dir, i, 'model.pth')
        hps = utils.get_hparams_from_file(m['config_path'])
        m['actors'] = [f"{sid}:{name}" for sid, name in enumerate(hps.speakers) if name != "None"]
        rs.append(m)

    return rs

def get_all_paths(input_dir, voice_ext, image_ext):
    rs = project.get_list(input_dir, voice_ext, image_ext)
    all_paths = []
    for r in rs:
        if not r['voice']:
            continue
        all_paths.append(r['voice'])
    return all_paths

def reload_table(model_dir):
    rs = get_list(model_dir)
    return [table_html(rs)]

def table_html(rs):
    code = ''
    for r in rs:
        code += f"""
        <table>
            <tbody>
        """
        for k in ['title', 'cover_path', 'author', 'lang', 'example', 'config_path', 'model_path']:
            if not k in r:
                continue
            code += f"<tr><th>{k}</th><td>{r[k]}</td></tr>"

        code += """
            </tbody>
        </table>
        """

        if not r['actors']:
            continue

        code += f"""
        <table>
            <thead>
                <tr>
                    <th>name</th>
                </tr>
            </thead>
            <tbody>
        """
        for a in r['actors']:
            code += f"""
                <tr>
                    <td>{r['model_id']}:{a}</td>
                </tr>
                """

        code += """
            </tbody>
        </table>
        """

    return code
