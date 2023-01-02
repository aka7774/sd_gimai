import os
import shutil
import pathlib
import json
import glob
import PIL as Image

def default_input_dir():
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'project')
    return filepath

def default_build_dir():
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'build')
    return filepath

def mainovel_dir():
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'mainovel')
    return filepath

def get_list(dir, voice_ext, image_ext):
    rs = []
    
    for filepath in glob.glob(f"{dir}/**/s[0-9][0-9][0-9].txt", recursive=True):
        scene = os.path.splitext(os.path.basename(filepath))[0]
        filedir = os.path.dirname(filepath)
        line = 1
        with open(filepath, 'r', encoding='utf-8') as f:
            for l in f:
                li = l.rstrip("\r\n").split(',')

                r = {}
                r['scene'] = scene
                r['line'] = 'm'+str(line).zfill(3)
                r['title'] = r['scene']+r['line']
                r['name'] = li[0]
                r['text'] = li[1]
                voice = glob.glob(f"{filedir}/{str(line).zfill(3)}*.{voice_ext}")
                r['voice'] = voice[0].replace(os.sep, '/') if len(voice) else ''
                image = glob.glob(f"{dir}/**/{r['title']}.{image_ext}", recursive=True)
                r['image'] = image[0].replace(os.sep, '/') if len(image) else ''

                rs.append(r)
                line += 1
    return rs

def build(input_dir, voice_ext, image_ext, build_dir):
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    data = {}
    data['config'] = {}
    data['config']['title'] = ''
    data['config']['audioInterval'] = ''
    data['config']['credit'] = ''
    data['voices'] = {}

    input_json = os.path.join(input_dir, 'mainovel.json')
    if os.path.exists(input_json):
        with open(input_json, 'r', encoding='utf-8') as f:
            data = json.load(f)

    null_voice = os.path.join(mainovel_dir(), f"m000.{voice_ext}")

    data['config']['sceneCodeFormat'] = '000'
    data['config']['messageCodeFormat'] = '000'
    data['config']['imageFormat'] = image_ext
    data['config']['audioFormat'] = voice_ext
    data['scenes'] = []
    rs = get_list(input_dir, voice_ext, image_ext)
    for i in range(0, 999):
        scene = 's'+str(i).zfill(3)
        voice_dir = os.path.join(build_dir, voice_ext, scene)
        if not os.path.exists(voice_dir):
            os.makedirs(voice_dir)
        image_dir = os.path.join(build_dir, image_ext, scene)
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        s = {}
        s['sceneName'] = ''
        s['messages'] = []
        for r in rs:
            if r['scene'] == scene:
                # indexのズレ補正
                if not len(s['messages']):
                    s['messages'].append('')
                    shutil.copy(null_voice, os.path.join(voice_dir, scene+'m000.'+voice_ext))
                    shutil.copy(r['image'], os.path.join(image_dir, scene+'m000.'+image_ext))
                s['messages'].append(r['text'])
                if r['voice']:
                    shutil.copy(r['voice'], os.path.join(voice_dir, f"{r['title']}.{voice_ext}"))
                if r['image']:
                    shutil.copy(r['image'], os.path.join(image_dir, f"{r['title']}.{image_ext}"))
        if not len(s['messages']):
            break
        data['scenes'].append(s)

    filepath = os.path.join(build_dir, 'mainovel.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent="\t", ensure_ascii=False)

    mainovel_files = [
    'server.bat',
    'index.html',
    'js/MaiNovel.js',
    'js/MaiNovelPlayer.js',
    ]
    js_dir = os.path.join(build_dir, 'js')
    if not os.path.exists(js_dir):
        os.makedirs(js_dir)

    for file in mainovel_files:
        shutil.copy(os.path.join(mainovel_dir(), file), os.path.join(build_dir, file))

    return 'saved.'

def show_voice(path):
    return path

def show_image(path):
    return path

def reload_table(input_dir, voice_ext, image_ext):
    rs = get_list(input_dir, voice_ext, image_ext)
    return [table_html(rs)]

def table_html(rs):
    code = f"""
    <table>
        <thead>
            <tr>
                <th>scene</th>
                <th>line</th>
                <th>name</th>
                <th>text</th>
                <th>voice</th>
                <th>image</th>
            </tr>
        </thead>
        <tbody>
    """

    for r in rs:
        voice = f"""
                <td><input onclick="show_voice(this, '{r['voice']}')" type="button" value="voice" class="gr-button gr-button-lg gr-button-secondary"></td>
                """ if r['voice'] else '<td></td>'
        image = f"""
                <td><input onclick="show_image(this, '{r['image']}')" type="button" value="image" class="gr-button gr-button-lg gr-button-secondary"></td>
                """ if r['image'] else '<td></td>'

        code += f"""
            <tr class="gimai_row" data-title="{r['title']}">
                <td>{r['scene']}</td>
                <td>{r['line']}</td>
                <td>{r['name']}</td>
                <td>{r['text']}</td>
                {voice}
                {image}
            </tr>
            """

    code += """
        </tbody>
    </table>
    """

    return code
