from pathlib import Path

import yaml

# Global settings object that can be used across whole application.
with open(Path(__file__).parent.parent.parent / 'config' / 'config.yml', 'r') as f:
    settings = yaml.safe_load(f)
