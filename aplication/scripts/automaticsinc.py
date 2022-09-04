from datetime import datetime, timedelta
from .utilidades_db import guarda_citas, guarda_articulos

ahora = datetime.now()
inicio=(ahora-timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
fin=(ahora+timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%SZ')
guarda_articulos()
guarda_citas(inicio, fin,'system')
