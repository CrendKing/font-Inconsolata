import shutil
import subprocess

if __name__ == '__main__':
    subprocess.check_call(['uv.exe', 'run', '.venv/Scripts/gftools-builder.py', 'sources/config.yaml'])

    # autohint for personal taste
    # since we have to use a earlier version of gftools to build fonts, which doesn't include the autohint script, run it from another venv
    subprocess.run(['uv.exe', '--project', 'D:/Development/Python/Font', 'run', 'gftools', 'autohint', '--auto-script', 'fonts/variable/Inconsolata[wdth,wght].ttf'])

    shutil.rmtree('sources/master_ufo', ignore_errors=True)
