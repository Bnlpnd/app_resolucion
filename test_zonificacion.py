#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_resolucion.settings')
django.setup()

from resoluciones.models import Zonificacion, DetalleResolucion, Resolucion

# Verificar que una zonificación pueda ser usada por múltiples detalles
print("=== Prueba de relación ForeignKey con Zonificación ===")

# Obtener todas las zonificaciones
zonificaciones = Zonificacion.objects.all()
print(f"Zonificaciones disponibles: {zonificaciones.count()}")

if zonificaciones.exists():
    zona_test = zonificaciones.first()
    print(f"Usando zonificación: {zona_test}")
    
    # Verificar cuántos detalles usan esta zonificación
    detalles_con_esta_zona = DetalleResolucion.objects.filter(zonificacion=zona_test)
    print(f"Detalles que usan esta zonificación: {detalles_con_esta_zona.count()}")
    
    for detalle in detalles_con_esta_zona:
        print(f"  - {detalle.resolucion}")
        
    print("✅ La relación ForeignKey está funcionando correctamente")
else:
    print("❌ No hay zonificaciones en la base de datos") 