import os

from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


def create_zip(path):
    with ZipFile(f'{path}.zip', 'w', ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(path):
            for f in files:
                print(f'Zipping {f}...')
                zipf.write(os.path.join(root, f))


def make_zipfile(zip_file_path, folder_or_file_to_zip, exclude_function=None):
    """Create an archive with exclusive files or directories. Adapted from shutil._make_zipfile.

    :param zip_file_path: Path of zip file to create.
    :param folder_or_file_to_zip: Directory or file that will be zipped.
    :param exclude_function: Function of exclude files or directories
    """
    with ZipFile(zip_file_path, "w") as zf:
        if os.path.isfile(folder_or_file_to_zip):
            zf.write(folder_or_file_to_zip, os.path.basename(folder_or_file_to_zip))
        else:
            for dirpath, dirnames, filenames in os.walk(folder_or_file_to_zip):
                relative_dirpath = os.path.relpath(dirpath, folder_or_file_to_zip)
                for name in sorted(dirnames):
                    full_path = os.path.normpath(os.path.join(dirpath, name))
                    relative_path = os.path.normpath(os.path.join(relative_dirpath, name))
                    if exclude_function and exclude_function(full_path):
                        continue
                    zf.write(full_path, relative_path)
                for name in filenames:
                    full_path = os.path.normpath(os.path.join(dirpath, name))
                    relative_path = os.path.normpath(os.path.join(relative_dirpath, name))
                    if exclude_function and exclude_function(full_path):
                        continue
                    if os.path.isfile(full_path):
                        zf.write(full_path, relative_path)


if __name__ == '__main__':
    for p in Path('.').iterdir():
        if p.is_dir():
            print(f'Processing {p} ...')
            make_zipfile(
                    zip_file_path=str(p) + '.zip',
                    folder_or_file_to_zip=p,
            )
