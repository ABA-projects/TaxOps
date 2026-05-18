from main import app as _api  # noqa: F401
from starlette.applications import Starlette
from starlette.routing import Mount

# Vercel experimentalServices forwards the FULL path (including /_/web prefix)
# to this service without stripping it.  Mount FastAPI at /_/web so that
# GET /_/web/health → FastAPI sees /health, etc.
app = Starlette(routes=[Mount("/_/web", app=_api)])
