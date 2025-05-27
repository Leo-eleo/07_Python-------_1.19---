import os
from pathlib import Path
from .language_patterns import LANGUAGE_PATTERNS

def setup_project():
    base_dir = Path(__file__).parent.parent
    
    dirs = [
        'language_samples',
        'output',
        'temp',
        'manual',
        'logs'
    ]
    
    for dir_name in dirs:
        os.makedirs(base_dir / dir_name, exist_ok=True)

    # Create empty language sample files
    for language in LANGUAGE_PATTERNS.keys():
        sample_file = base_dir / 'language_samples' / f"{language.lower()}_sample.txt"
        if not sample_file.exists():
            sample_file.touch()

    print("Project structure created successfully!")

if __name__ == "__main__":
    setup_project()
