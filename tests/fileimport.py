'''
Import a file without executing the module path.
Used for testing modules separately from the server
without setting up server environment variables.
'''
import importlib
import os
import pathlib
import sys
import types

app_path = 'apps/text-synth/'

def import_module_from_path(path: os.PathLike) -> types.ModuleType:
    """Import a module from the given path."""
    module_path = pathlib.Path(path).resolve()
    module_name = module_path.stem  # 'path/x.py' -> 'x'
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def _import(filename):
    module = import_module_from_path(app_path + filename + '.py')

    return module
