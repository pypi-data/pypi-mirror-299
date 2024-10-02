import os
import click
import json
import shutil
import ctypes
from packaging.version import Version

ERROR_COLOR = '\033[91m' # Red
WARNING_COLOR = '\033[93m' # Yellow
SUCCESS_COLOR = '\033[92m' # Green
RESET_COLOR = '\033[0m' # Reset

CONFIG_PATH = r'exe-index.config' # Default config path

@click.command()
def new_index():
    '''
    Create a new index folder.
    '''
    obj = load_config()
    INDEX_PATH = obj.get('index-path')
    EXE_INDEX_SETTING_FILE = os.path.join(INDEX_PATH, 'exe-index.config')

    if not os.path.exists(INDEX_PATH):
        click.echo(f'{ERROR_COLOR}Index path does not exist.{RESET_COLOR}')
        return

    if os.path.exists(EXE_INDEX_SETTING_FILE):
        click.echo(f'{ERROR_COLOR}Index already exists, please run `exe-index publish` to publish the current exe to the index.{RESET_COLOR}')
        return

    # Create the index file and make it hidden windows
    with open(EXE_INDEX_SETTING_FILE, 'w') as f:
        f.write(json.dumps({}, indent=4))
    os.system(f'attrib +h "{EXE_INDEX_SETTING_FILE}"')

@click.group()
def cli():
    pass

@cli.command()
def init():
    '''
    Create a new config file with default values, if the file already exists, only missing values will be added.
    '''
    obj = load_config()
    with open(CONFIG_PATH, 'w') as f:
        f.write(json.dumps(obj, indent=4))

@cli.command()
def publish():
    '''
    Publish the current exe to the index.
    '''
    # Load the config file
    obj = load_config()
    EXE_NAME = obj.get('exe-name')
    EXE_PATH = os.path.abspath(obj.get('exe-path'))
    EXE_VERSION = obj.get('exe-version')
    INDEX_PATH = os.path.abspath(obj.get('index-path'))
    
    # Check if any values are missing
    ERROR_LIST = []
    if not EXE_NAME: ERROR_LIST.append('exe-name')
    if not EXE_PATH: ERROR_LIST.append('exe-path')
    if not EXE_VERSION: ERROR_LIST.append('exe-version')
    if not INDEX_PATH: ERROR_LIST.append('index-path')
    if ERROR_LIST: 
        click.echo(f'{ERROR_COLOR}Missing values in config file: {", ".join(ERROR_LIST)}{RESET_COLOR}')
        return

    # Check if the index exists
    EXE_INDEX_SETTING_FILE = os.path.join(INDEX_PATH, 'exe-index.config')
    if not os.path.exists(EXE_INDEX_SETTING_FILE):
        click.echo(f'{ERROR_COLOR}Index does not exist, please run `exe-new-index` to create a new index.{RESET_COLOR}')
        return

    upload_file(EXE_NAME, EXE_PATH, EXE_VERSION, INDEX_PATH)

def upload_file(exe_name: str, exe_path: str, exe_version: str, index_path: str):
    '''
    Upload the exe to the index.
    '''
    package_path = os.path.join(index_path, f'_{exe_name}')
    upload_target = os.path.join(index_path, f'{exe_name}.exe')
    upload_versioned_target = os.path.join(package_path, f'{exe_name}_v{exe_version}.exe')

    # Check if package path exists and create it if it does not
    if not os.path.exists(package_path):
        os.makedirs(package_path)
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ctypes.windll.kernel32.SetFileAttributesW(package_path, FILE_ATTRIBUTE_HIDDEN)
    
    # Check if the same version of the exe is already in the index
    exe_uid_files = os.listdir(package_path)
    if f'{exe_name}_v{exe_version}.exe' in exe_uid_files:
        click.echo(f'{ERROR_COLOR}Version {exe_version} of exe \'{exe_name}\' already exists in the index.{RESET_COLOR}')
        return
    
    # Copy the exe to the index
    shutil.copy(exe_path, upload_versioned_target)
    expose_stable_version(upload_target, package_path)

def expose_stable_version(upload_target: str, package_path: str):
    '''
    Expose the stable version of the exe.
    '''
    exe_list = os.listdir(package_path)
    exe_list = [{
        'name': x,
        'version': x.split('_v')[1].split('.exe')[0],
    } for x in exe_list]
    exe_list = sorted(exe_list, key=lambda x: Version(x['version']), reverse=True)
    exe_list = [x for x in exe_list if Version(x['version']).is_prerelease == False]
    stable_exe = exe_list[0]["name"]
    shutil.copy(os.path.join(package_path, stable_exe), upload_target)

@cli.command()
def config():
    '''
    Print the current config file values. Usefull for debugging.
    '''
    obj = load_config()
    click.echo('Current Config:')
    click.echo(json.dumps(obj, indent=4))

def load_config():
    obj: dict = {
        'exe-name': None,
        'exe-path': None,
        'exe-version': None,
        'index-path': None,
        'thrid-party-configs': {
            'ppm-config-path': '.proj.config',
            },
        }
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            _obj: dict = json.loads(f.read())
            obj = {**obj, **_obj}

    ppm_config = obj.get('thrid-party-configs', {}).get('ppm-config-path')
    if ppm_config and os.path.exists(ppm_config):
        try:
            import python_project_manager as ppm
            with open(ppm_config, 'r') as f:
                file_text = f.read()
                _obj: dict = json.loads(ppm.Config.parse(file_text, json.loads(file_text)))
                obj = {**obj, **{
                    "exe-name": _obj.get("exe-index", {}).get("exe-name") or obj.get("exe-name"),
                    "exe-version": _obj.get("exe-index", {}).get("exe-version") or obj.get("exe-version"),
                    "exe-path": _obj.get("exe-index", {}).get("exe-path") or obj.get("exe-path"),
                    "index-path": _obj.get("exe-index", {}).get("index-path") or obj.get("index-path"),
                }}
        except ImportError:
            click.echo(f'{WARNING_COLOR}Python Project Manager not found, skipping config file.{RESET_COLOR}')

    return obj