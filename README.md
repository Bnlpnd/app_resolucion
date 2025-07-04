# Sistema de Resoluciones de Licencias

Sistema Django para gestión de resoluciones de licencias de construcción con dos perfiles: **Obras** y **Fiscalización**.

## 🚀 Instalación Rápida

1. **Aplicar migraciones:**
   ```bash
   python manage.py migrate
   ```

2. **Configurar sistema:**
   ```bash
   python manage.py setup_sistema
   ```

3. **Crear superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

4. **Ejecutar servidor:**
   ```bash
   python manage.py runserver
   ```

5. **Acceder:**
   - App: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

## 👥 Configuración de Usuarios

1. Registrarse en: http://localhost:8000/registro/
2. Desde admin, asignar usuario a grupo:
   - **Obras**: Crea y edita sus resoluciones
   - **Fiscalización**: Ve todas las resoluciones

## ✨ Características

- **Autenticación completa** (login/logout/registro)
- **Dos perfiles** con permisos específicos
- **CRUD de resoluciones** con validaciones
- **Responsable flexible** (seleccionar o crear nuevo)
- **Filtros avanzados** para búsqueda
- **Interfaz Bootstrap 5** responsiva
- **Panel admin** personalizado

## 📋 Modelos

- **Resolucion**: Datos principales de la resolución
- **DetalleResolucion**: Información técnica de construcción  
- **ResponsableObra**: Profesionales responsables
- **Zonificacion**: Datos de ubicación
- **LicenciaUso**: Tipos de licencias

## 🎯 Funcionalidades por Perfil

### Obras
- ✅ Crear nuevas resoluciones
- ✅ Ver/editar solo sus resoluciones
- ✅ Dashboard con accesos rápidos

### Fiscalización  
- ✅ Ver todas las resoluciones
- ✅ Filtros por múltiples criterios
- ✅ Opciones de exportación
- ❌ Solo lectura

## 🛠 Estructura

```
resoluciones/
├── models.py           # Modelos de datos
├── views.py            # Vistas con control de permisos
├── forms.py            # Formularios validados
├── templates/          # Templates Bootstrap
└── management/         # Comando setup_sistema
```

## 📝 Uso

1. **Registro**: Los usuarios se registran y admin asigna permisos
2. **Obras**: Accede a dashboard, crea/edita resoluciones
3. **Fiscalización**: Ve listado completo con filtros
4. **Responsables**: Sistema flexible para seleccionar o crear nuevos

## 🔧 Tecnologías

- Django 5.2 + Bootstrap 5
- SQLite (configurable)
- Sistema auth integrado
- Vistas basadas en clases

---
**Sistema listo para usar! 🎉** 