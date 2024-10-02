import os
import click
import python_project_manager

@click.command()
@click.argument('project_name', type=str, required=True)
def exe_setup(project_name):
    if len(os.listdir(os.getcwd())) != 0:
        print('Project already initialized')
        return
    
    _src_path = 'src'
    _version = '0.0.0b1'
    
    initializer = python_project_manager.Initializer()
    initializer.AddConfigValue('project_name', project_name)
    initializer.AddConfigValue('src_dir', _src_path)
    initializer.AddConfigValue('include_paths', [_src_path])
    initializer.AddConfigValue('version', _version)
    initializer.AddConfigValue('scripts.start', r'python Application.py')
    initializer.AddConfigValue('scripts.build', r'ppm run __sync && ppm run __build')
    initializer.AddConfigValue('scripts.__sync', r'python dev_scripts/sync.py')
    initializer.AddConfigValue('scripts.__build', r'pyinstaller Application.py --noconfirm --clean --onefile --name %project_name%_v%version% --add-data %src_dir%/resources:. --add-data Application.env:.')
    initializer.AddFolder(f'{_src_path}/resources')
    initializer.AddFolder('dev_scripts')
    initializer.AddFile(f'Application.py',
'''
\'\'\'
    This file is the entry point of the application.

    It is responsible for setting up the file paths, loading the environment variables, and launching the application.

    Only handles exceptions that occur during the setup process all other exceptions should be handled by the application.

    The application should be launched by running this file.

    `resource` is the directory that contains the application files.

    `Application.env` is the environment file that contains required environment variables.
\'\'\'

import traceback
try:
    import os
    import sys
    import ctypes
    from dotenv import load_dotenv as __load_dotenv
    from pathlib import Path as __Path

#region ApplicationSetup
    class Paths:
        ResourcePath: str
        LocalPath: str
        HiddenPath: str

        @staticmethod
        def GetResource(path: str) -> str:
            \'\'\'
            Returns the full path of a file in the resource directory.
            \'\'\'
            return os.path.join(Paths.ResourcePath, path)
        
        @staticmethod
        def GetLocal(path: str) -> str:
            \'\'\'
            Returns the full path of a file in the user's local directory.
            \'\'\'
            return os.path.join(Paths.LocalPath, path)
        
        @staticmethod
        def GetHidden(path: str) -> str:
            \'\'\'
            Returns the full path of a file in the hidden directory.
            \'\'\'
            return os.path.join(Paths.HiddenPath, path)

        @staticmethod
        def Open() -> None:
            \'\'\'
            Opens to the application's directory.
            \'\'\'
            os.startfile(Paths.LocalPath)
        
        @staticmethod
        def Dump():
            for key in dir(Paths):
                _value = getattr(Paths, key)
                if key.startswith('__'): continue
                _type = type(_value).__name__
                if _type == 'module': continue
                print(f'\\033[93m{Paths.__name__}.{key}:\\033[0m \\033[94m{_type}\\033[0m = \\033[92m{_value}\\033[0m')

    # Pre .env load
    IsExecutable = hasattr(sys, 'frozen')
    Paths.ResourcePath = sys._MEIPASS if IsExecutable else os.path.abspath('.')

    # Load .env
    __load_dotenv(Paths.GetResource('.env'))
    __load_dotenv(Paths.GetResource('Application.env'))
    Name: str | None = os.environ.get('APP_NAME')
    Version:  str | None = os.environ.get('APP_VERSION')
    __auto_retry: bool = os.environ.get('APP_AUTO_RETRY', 'true').lower() == 'true'
    __env_errors = []
    if Name is None: __env_errors.append('APP_NAME')
    if Version is None: __env_errors.append('APP_VERSION')
    if len(__env_errors) > 0:
        raise Exception(f"Missing environment variables: {', '.join(__env_errors)}")

    # Post .env load
    __user_path = os.path.join(__Path.home(), 'AppData\\\\Local') if IsExecutable else os.path.abspath('./__Local__')
    Paths.LocalPath = os.path.join(__user_path, Name)
    Paths.HiddenPath = os.path.join(__user_path, Name, '.data')

    def __create_directory(path: str, hidden: bool):
        if not os.path.exists(path):
            os.makedirs(path)
            if hidden:
                ctypes.windll.kernel32.SetFileAttributesW(path, 2)
    __create_directory(Paths.LocalPath, False)
    __create_directory(Paths.HiddenPath, True)
            

    def Dump():
        import Application
        # print each key(in yellow), type(in blue) and value(in green) in this format: key: type = value
        for key in dir(Application):
            _value = getattr(Application, key)
            if key.startswith('__'): continue
            _is_class = str(_value).startswith('<class ')
            _type = type(_value).__name__
            if _type == 'module': continue
            print(f'\\033[93m{key}:\\033[0m \\033[94m{_type}\\033[0m = \\033[92m{_value}\\033[0m')
            if _is_class and hasattr(_value, 'Dump'):
                try: _value.Dump()
                except: print(f'\\033[91mFailed to dump {key}!\\033[0m')
#endregion

#region ApplicationLauncher
    def __launch_application():
        from src.main import main
        while True:
            try:
                main()
                break
            except Exception as e:
                print("\\n\\033[91mApplication crashed with error:\\033[0m")
                traceback.print_exc()
                if not __auto_retry:
                    input("Press Enter to exit...")
                    exit(1)
                input("Press Enter to restart...")

    def __launcher_setup():
        try:
            print('\\033[92m' + Name + ' v' + Version + '\\033[0m')
            __launch_application()
        except Exception as e:
            print("\\n\\033[91mLauncher failed to start application with error:\\033[0m")
            traceback.print_exc()
            input("Press Enter to exit...")
            exit(1)

    if __name__ == '__main__':
        __launcher_setup()
        input("\\n\\033[94mApplication exited successfully!\\033[0m\\nPress Enter to exit...")
        exit(0)
#endregion
except Exception as e:
    print("\\n\\033[91mLauncher crashed with error:\\033[0m")
    traceback.print_exc()
    input("Press Enter to exit...")
''')
    initializer.AddFile(f'Application.env',
f'''
APP_NAME={project_name} # Application Name
APP_VERSION={_version} # Application Version
APP_AUTO_RETRY=true # If the applicaion crashes, launcher will relaunch the application
''')
    initializer.AddFile(f'{_src_path}/main.py',
r'''
import Application

def main(): # DO NOT REMOVE THIS DEFINITION, IT IS USED BY THE LAUNCHER TO START THE APPLICATION
    print(f'Hello from {Application.Name} v{Application.Version}!')
    # print(Application.Paths.Open())
''')
    initializer.AddFile(f'dev_scripts/sync.py',
r'''
import json
import re
with open('.proj.config', 'r') as config:
    config_text = config.read()
    config_data = json.loads(config_text)
    config_version = config_data['version']
    print(config_version)
    env_text: str
    with open('Application.env', 'r') as env:
        env_text = env.read()
        env_version_regex = r'(?P<a>^APP_VERSION=\s*)(?P<v>[^#]*?)(?P<b>\s*#.*?$|$)'
        env_text = re.sub(env_version_regex, r'\g<a>' + config_version + r'\g<b>', env_text, flags=re.MULTILINE)
        print(env_text)
    with open('Application.env', 'w') as env:
        env.write(env_text)
''')
    initializer.AddFile('.gitignore',
'''
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
*.manifest
*.spec
pip-log.txt
pip-delete-this-directory.txt
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/
*.mo
*.pot
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
instance/
.webassets-cache
.scrapy
docs/_build/
.pybuilder/
target/
.ipynb_checkpoints
profile_default/
ipython_config.py
.pdm.toml
.pdm-python
.pdm-build/
__pypackages__/
celerybeat-schedule
celerybeat.pid
*.sage.py
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
.spyderproject
.spyproject
.ropeproject
/site
.mypy_cache/
.dmypy.json
dmypy.json
.pyre/
.pytype/
cython_debug/
!Application.env
__Local__/
''')
    
    initializer.Initialize()
    python_project_manager.RunCommand('python -m venv venv', use_venv=False)
    python_project_manager.RunCommand('ppm install python-dotenv==1.0.1', use_venv=True)
    python_project_manager.RunCommand('ppm install pyinstaller==6.10.0 -d', use_venv=True)
    print(f'Project {project_name} created')