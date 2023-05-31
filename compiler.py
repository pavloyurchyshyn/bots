import os
import time
import datetime
import shutil
import subprocess
from pathlib import Path
from settings.version import VERSION
import traceback

start = time.time()
try:
    GAME_ICO = 'game.ico'
    SERVER_ICO = 'server.ico'
    if __name__ == '__main__':
        root = Path(__file__).parent
        out_folder = root / 'compiled_versions'
        launch = root / 'launch.py'
        config = root / 'compile_conf.json'

        dist_folder = root / 'dist'
        build_folder = root / 'build'
        launch_spec_file = root / 'launch.spec'
        server_spec_file = root / 'server.spec'
        try:
            if not out_folder.exists():
                out_folder.mkdir()

            compiled_out = Path(out_folder, f'v{VERSION}')
            # compiled_out = Path(out_folder, f'v{VERSION}_{datetime.datetime.now().strftime("%m_%d_%Y_%H_%M")}')
            compiled_exe = compiled_out / 'run.exe'

            if compiled_out.exists():
                shutil.rmtree(compiled_out)
            compiled_out.mkdir()

            subprocess.call('pyinstaller '
                            '--noconfirm --onefile --windowed '
                            f'--icon "{GAME_ICO}" '
                            '--add-data "E:/nastilna_gra_refactor/localization;localization/" '
                            '--add-data "E:/nastilna_gra_refactor/sounds;sounds/" '
                            '--add-data "E:/nastilna_gra_refactor/textures;textures/"  '
                            '"E:/nastilna_gra_refactor/launch.py"')

            shutil.copy(dist_folder / 'launch.exe', compiled_exe)

        except Exception as e:
            print(e)
            print(traceback.format_exc())
        else:

            server_exe = dist_folder / 'server.exe'
            server_exe_dst = compiled_out / 'server.exe'
            subprocess.call('pyinstaller '
                            '--noconfirm --onefile --console '
                            f'--icon "{SERVER_ICO}"  '
                            '"E:/nastilna_gra_refactor/server.py"')
            shutil.copy(server_exe, server_exe_dst)

            for folder in ('localization', 'sounds', 'textures', 'fonts'):
                shutil.copytree(root / folder, compiled_out / folder)

            for file in (GAME_ICO, SERVER_ICO):
                shutil.copy(root / file, compiled_out / file)

        finally:
            if dist_folder.exists():
                shutil.rmtree(dist_folder)
            if build_folder.exists():
                shutil.rmtree(build_folder)
            if launch_spec_file.exists():
                os.remove(launch_spec_file)
            if server_spec_file.exists():
                os.remove(server_spec_file)
except Exception as e:
    print(e)
    print(traceback.format_exc())
else:
    time_d = round(time.time() - start, 2)
    with open(compiled_out / 'META.txt', 'w') as f:
        data = f'time {time_d}\n'\
        f'version {VERSION}\n' \
        f'date {datetime.datetime.now().strftime("%d:%m:%Y %H:%M:%S")}\n'
        f.write(data)
time_d = round(time.time() - start, 2)
print(f'Time spent: {time_d} seconds.')