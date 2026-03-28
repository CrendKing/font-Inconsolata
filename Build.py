import os
import shutil
import subprocess

if __name__ == '__main__':
    subprocess.check_call(['gftools', 'builder', 'sources/config.yaml'])

    # autohint for personal taste
    # since we have to use a earlier version of gftools to build fonts, which doesn't include the autohint script, run it from another venv
    subprocess.run(['uv', '--project', 'D:/Development/Python/Font', 'run', 'gftools', 'autohint', '--auto-script', 'fonts/variable/Inconsolata[wdth,wght].ttf'])

    os.remove('sources/build.ninja')
    os.remove('sources/.ninja_log')
    shutil.rmtree('sources/master_ufo', ignore_errors=True)
