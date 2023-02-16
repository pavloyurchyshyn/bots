import os
import shutil
import datetime
import subprocess
from pathlib import Path
from settings.version import VERSION

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

        compiled_out = Path(out_folder, f'v{VERSION}')  # _{datetime.datetime.now().strftime("%m_%d_%Y_%H_%M")}')
        if compiled_out.exists():
            shutil.rmtree(compiled_out)
        # args = ['auto-py-to-exe',
        #         launch.as_posix(),
        #         '-c', config.as_posix(),
        #         '--output-dir', compiled_out.as_posix(),
        #         ]
        # subprocess.call(args)
        subprocess.call('pyinstaller '
                        '--noconfirm --onedir --windowed '
                        '--add-data "E:/nastilna_gra_refactor/localization;localization/" '
                        '--add-data "E:/nastilna_gra_refactor/sounds;sounds/" '
                        '--add-data "E:/nastilna_gra_refactor/textures;textures/"  '
                        '"E:/nastilna_gra_refactor/launch.py"')

        shutil.copytree(dist_folder / 'launch', compiled_out)
    except Exception as e:
        print(e)
    else:
        server_exe = dist_folder / 'server.exe'
        server_exe_dst = compiled_out / 'server.exe'
        subprocess.call('pyinstaller --noconfirm --onefile --console  "E:/nastilna_gra_refactor/server.py"')
        shutil.copy(server_exe, server_exe_dst)
    finally:
        if dist_folder.exists():
            shutil.rmtree(dist_folder)
        if build_folder.exists():
            shutil.rmtree(build_folder)
        if launch_spec_file.exists():
            os.remove(launch_spec_file)
        if server_spec_file.exists():
            os.remove(server_spec_file)
