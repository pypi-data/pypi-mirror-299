import os
from importlib import resources
from pathlib import Path


class Assets:
    with resources.files('nikassets.helper').joinpath('assets') as asset_path:
        assets_folder = str(asset_path)
    if not os.path.exists(assets_folder):
        assets_folder = os.path.join(os.getcwd(), 'assets')
    if not os.path.exists(assets_folder):
        pwd = Path(os.getcwd()).parent
        for folders in pwd.iterdir():
            if folders.is_dir():
                if folders.name == "assets":
                    assets_folder = str(folders)
                    break
    cwd = assets_folder + os.path.sep

    @staticmethod
    def get(file_name):
        return Assets.cwd + file_name