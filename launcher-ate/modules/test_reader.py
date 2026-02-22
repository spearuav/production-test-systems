# launcher-ate/modules/test_reader.py
from modules.util import get_base_dir


class TestReader:
    """Reads and validates test configurations"""
    
    def __init__(self):
        self.base_dir = get_base_dir()
        self.tests_dir = self.base_dir / "tests"
        self.actions_dir = self.base_dir / "actions"
        self.tests = []
        self.actions = []
        self.error = False
        
    def load(self):
        """Load test information and validate required files"""
        self.error = True
        
        # Validate directories
        if not self.tests_dir.exists():
            raise FileNotFoundError(f"Tests directory not found: {self.tests_dir}")
        if not self.actions_dir.exists():
            raise FileNotFoundError(f"Actions directory not found: {self.actions_dir}")
        
        # Validate required files
        if not (self.actions_dir / "setup.py").exists():
            raise FileNotFoundError(f"setup.py not found in actions directory: {self.actions_dir}")
        if not (self.tests_dir / "iperf.py").exists():
            raise FileNotFoundError(f"iperf.py not found in tests directory: {self.tests_dir}")
        
        # Get sorted lists of tests and actions
        self.tests = self.get_sorted_files(self.tests_dir)
        self.actions = self.get_sorted_files(self.actions_dir)
        
        # Update counts
        self.test_count = len(self.tests)
        self.action_count = len(self.actions)
        
        # If we get here, all required files exist
        self.error = False

    @staticmethod
    def get_sorted_files(directory, exclude_files=None):
        """
        Get a sorted list of files in the given directory, excluding specified files.

        Args:
            directory (Path): The directory to search for files.
            exclude_files (list, optional): List of file names to exclude. Defaults to None.

        Returns:
            list: Sorted list of file names in the directory, excluding specified files.
        """
        if not directory.exists():
            return []
        
        exclude_files = set(exclude_files or [])
        return sorted(
            [item.name for item in directory.iterdir() if item.is_file() and item.name not in exclude_files]
        )
