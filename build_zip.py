import os

from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


def create_zip(path):
    with ZipFile(f'{path}.zip', 'w', ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(path):
            for f in files:
                print(f'Zipping {f}...')
                zipf.write(os.path.join(root, f))


if __name__ == '__main__':
    for p in Path('.').iterdir():
        if p.is_dir():
            print(f'Processing {p} ...')
            create_zip(p)
