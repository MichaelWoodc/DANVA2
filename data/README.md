# DANVAII

# install errors on 2/15/2023
C:\CODE\1_vscode\DANVAII\dist>maingraphed.exe
Python path configuration:
  PYTHONHOME = (not set)
  PYTHONPATH = (not set)
  program name = 'C:\CODE\1_vscode\DANVAII\dist\MainGraphed.exe'
  isolated = 1
  environment = 0
  user site = 0
  import site = 0
  sys._base_executable = 'C:\\CODE\\1_vscode\\DANVAII\\dist\\MainGraphed.exe'
  sys.base_prefix = ''
  sys.base_exec_prefix = ''
  sys.executable = 'C:\\CODE\\1_vscode\\DANVAII\\dist\\MainGraphed.exe'
  sys.prefix = ''
  sys.exec_prefix = ''
  sys.path = [
    'C:\\CODE\\1_vscode\\DANVAII\\dist\\library.zip',
  ]
Fatal Python error: init_fs_encoding: failed to get the Python codec of the filesystem encoding
Python runtime state: core initialized
ModuleNotFoundError: No module named 'encodings'

Nuitka:WARNING: Using very slow fallback for ordered sets, please install 'ordered-set' PyPI package for best Python compile time performance.
Nuitka:INFO: Starting Python compilation with Nuitka '1.4.7' on Python '3.8' commercial grade 'not installed'.
Nuitka-Plugins:WARNING: Use '--enable-plugin=pyqt5' for: Inclusion of Qt plugins.
python -m nuitka --standalone --enable-plugin=pyqt5 --include-data-files --include-data-dir 
--include-plugin-directory=mods maingraphed.py

try to add: --noinclude-default-mode=error  (this actually just ignores warnings)
try to add: --nofollow-import-to=IPython
--include-data-files=/data/*=data/


Is this important? "Nuitka-Plugins:INFO: gevent:     Disabling 'gevent' greenlet tree tracking."

--include-data-files=/data/*=data/
--include-plugin-directory=mods