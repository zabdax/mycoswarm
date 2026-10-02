"""pytest bootstrap: expose src/ for test imports (repo runs pytest from root)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
