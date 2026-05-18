import sys
from pathlib import Path

# includeFiles bundles services/, db/, pipeline/, exogenas/ into /var/task/ (this file's dir).
# Explicitly add it so main.py's cross-package imports resolve correctly on Vercel.
_here = str(Path(__file__).parent)
if _here not in sys.path:
    sys.path.insert(0, _here)

from main import app  # noqa: F401  — Vercel ASGI entry point
