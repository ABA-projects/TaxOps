import sys
from pathlib import Path
_api = str(Path(__file__).parent / "api")
if _api not in sys.path:
    sys.path.insert(0, _api)

# Re-export para compatibilidad con app_v2.py
from services.chatbot import (  # noqa: F401
    responder,
    _tool_consultar_iva_mes,
    _tool_top_proveedores,
    _tool_buscar_factura,
    _tool_resumen_errores,
    _tool_resumen_general,
)
