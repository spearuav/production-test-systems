import csv
from pathlib import Path
from datetime import datetime

class ATRWriter:
    def __init__(self, atr_dir: Path, test_names: list):
        self.atr_dir = atr_dir
        self.test_names = test_names
        self.atr_file = self._get_or_create_atr_file()

    def _get_or_create_atr_file(self):
        """Find the latest ATR file or create a new one if necessary."""
        self.atr_dir.mkdir(parents=True, exist_ok=True)
        existing_files = sorted(self.atr_dir.glob("ATR_*.csv"))

        if existing_files:
            latest_file = existing_files[-1]
            with open(latest_file, "r") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if header and set(self.test_names).issubset(header):
                    return latest_file

        # Create a new ATR file with an incremented name
        new_file_name = f"ATR_{len(existing_files) + 1}.csv"
        new_file_path = self.atr_dir / new_file_name
        self._create_new_atr_file(new_file_path)
        return new_file_path

    def _create_new_atr_file(self, file_path):
        """Create a new ATR file with the appropriate header."""
        header = ["Number", "Launcher SN", "Date Performed", "Performed By", "Conclusion", "Comments"] + self.test_names
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)

    def append_entry(self, number, launcher_sn, performed_by, conclusion, comments, test_results):
        """Append a new entry to the ATR file."""
        date_performed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [number, launcher_sn, date_performed, performed_by, conclusion, comments] + test_results
        with open(self.atr_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def finalize(self):
        """Allow the operator to input conclusions and finalize the ATR file."""
        conclusion = input("Enter the conclusion for this test run: ")
        comments = input("Enter any additional comments: ")
        return conclusion, comments