"""Fail CI when detect-secrets reports findings without printing secret values."""
import json
import sys
from pathlib import Path
results = json.loads(Path(sys.argv[1]).read_text())['results']
if results:
    print('Potential secrets in:', ', '.join(sorted(results)))
    raise SystemExit(1)
