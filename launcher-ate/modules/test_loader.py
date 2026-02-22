import importlib
import sys
from pathlib import Path

class TestLoader:
    def __init__(self, tests_dir: Path, actions_dir: Path):
        self.tests_dir = tests_dir
        self.actions_dir = actions_dir

    def load_test(self, name: str):
        return self._load_module(self.tests_dir, name)

    def load_action(self, name: str):
        return self._load_module(self.actions_dir, name)

    def _load_module(self, directory: Path, name: str):
        # Strip .py extension if present to avoid double extension
        if name.endswith('.py'):
            name = name[:-3]
        
        module_path = directory / f"{name}.py"
        if not module_path.exists():
            raise FileNotFoundError(f"Module {name} not found in {directory}")
        
        spec = importlib.util.spec_from_file_location(name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def unload_module(self, name: str):
        if name in sys.modules:
            del sys.modules[name]