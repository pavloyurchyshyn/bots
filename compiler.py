import os
import re
import shutil
import subprocess
import auto_py_to_exe
from pathlib import Path


def increase_version(versions: list):
    versions = versions.copy()

    v = versions[-1] + 1
    if v > 99:
        v = v - 100
        versions[-2] += 1
    versions[-1] = v
    if versions[-2] > 100:
        versions[-2] = versions[-2] - 100
        versions[0] += 1

    return versions


if __name__ == '__main__':
    root = Path(__file__).parent
    out_folder = root / 'compiled_versions'
    version_file = root / 'settings' / 'version.py'
    launch = root / 'launch.py'
    config = root / 'compile_conf.json'

    dest_folder = root / 'dist'

    if not out_folder.exists():
        out_folder.mkdir()

    version = version_file.read_text()
    version = version.split("'")[-2]
    vers = list(map(int, version.split('.')))
    vers = increase_version(vers)
    str_version = '.'.join(map(str, vers))

    version_file.write_text(f"VERSION = '{str_version}'\n")
    compiled_out = Path(out_folder, f'v{str_version}')
    args = ['pyinstaller',
            '--noconfirm', '--onedir', '--windowed',
            '--add-data', '"E:/nastilna_gra_refactor/sounds;sounds/"',
            '--add-data', '"E:/nastilna_gra_refactor/textures;textures/"',
            '--add-data', '"E:/nastilna_gra_refactor/localization;localization/"',
            '"E:/nastilna_gra_refactor/launch.py"',
            ]

    subprocess.call(args)

    shutil.copytree(dest_folder / 'launch', compiled_out)

    shutil.rmtree(dest_folder)
