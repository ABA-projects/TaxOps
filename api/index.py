import sys
from pathlib import Path

# Vercel entrypoint "." → this file is at /var/task/api/index.py
# Add api/ so 'from main import app' works (and 'from routers import ...' inside main.py)
# Add project root so 'from services import ...', 'from db import ...' work
_api_dir = Path(__file__).parent
_project_root = _api_dir.parent

for _p in (str(_api_dir), str(_project_root)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from main import app  # noqa: F401
