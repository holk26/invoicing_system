# Sistema de Facturación Electrónica

## Descripción del Proyecto
Sistema web para la gestión de facturación electrónica desarrollado para cumplir con los requerimientos de la DIAN (Dirección de Impuestos y Aduanas Nacionales) en Colombia. Esta aplicación permite a empresas generar, administrar y enviar facturas electrónicas, notas crédito y notas débito, asegurando el cumplimiento con las normativas fiscales vigentes.

## Desarrollado para
Universidad Politécnico Colombiano

## Características Principales

### Funcionalidades
- **Gestión de Usuarios**: Sistema de roles (Administrador, Operador, Contador) con autenticación de doble factor.
- **Gestión de Empresas**: Registro y administración de información corporativa, certificados digitales y régimen tributario.
- **Catálogo de Productos**: Administración completa de productos con control de inventario.
- **Facturación Electrónica**: Generación de facturas según los estándares UBL 2.1 de la DIAN.
- **Firma Digital**: Implementación de firmas digitales para la validación de documentos.
- **Notas Crédito/Débito**: Emisión de notas asociadas a facturas existentes.
- **Gestión de Clientes**: Base de datos completa de clientes y su información fiscal.
- **Modo Offline**: Capacidad para generar facturas sin conexión y sincronizarlas posteriormente.
- **Reportes**: Generación de informes de ventas y estado de facturación.
- **Auditoría**: Registro detallado de acciones realizadas en el sistema.

### Aspectos Técnicos
- **Framework**: Django 5.2
- **Base de Datos**: SQLite (escalable a PostgreSQL)
- **Frontend**: Bootstrap 5, JavaScript
- **Seguridad**: Implementación de protocolos HTTPS, CSRF y XSS
- **Interoperabilidad**: Integración con servicios web SOAP de la DIAN

## Requisitos del Sistema
- Python 3.11+
- Django 5.2+
- Zeep (para servicios SOAP)
- Otras dependencias especificadas en requirements.txt

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/holk26/invoicing_system.git
cd invoicing_system
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Aplicar migraciones:
```bash
python manage.py migrate
```

5. Generar datos de prueba (opcional):
```bash
python manage.py generate_sample_data
```

6. Iniciar servidor de desarrollo:
```bash
python manage.py runserver
```

## Estructura del Proyecto

```
invoicing_system/
├── core/                   # Aplicación principal
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Vistas y lógica de negocio
│   ├── forms.py            # Formularios
│   ├── urls.py             # Rutas URL
│   └── management/         # Comandos personalizados
├── invoicing_system/       # Configuración del proyecto
├── static/                 # Archivos estáticos (JS, CSS)
├── templates/              # Plantillas HTML
│   ├── core/               # Plantillas específicas
│   └── registration/       # Plantillas de autenticación
└── requirements.txt        # Dependencias del proyecto
```

## Requerimientos Funcionales Implementados

1. **RF01**: Sistema de autenticación con roles diferenciados y 2FA
2. **RF02**: Gestión de información empresarial y certificados digitales
3. **RF03**: Administración de productos y servicios con categorización
4. **RF04**: Generación de facturas electrónicas según estándares UBL 2.1
5. **RF05**: Validación de facturas con servicios web de la DIAN
6. **RF09**: Gestión completa de clientes y su información fiscal
7. **RF10**: Modo offline con sincronización posterior
8. **RF13**: Generación de notas crédito y débito
9. **RF14**: Auditoría de acciones en el sistema
10. **RF15**: Gestión de impuestos aplicables a productos

## Requerimientos No Funcionales Implementados

1. **RNF03**: Seguridad implementada con protocolos HTTPS, CSRF y XSS
2. **RNF13**: Sistema de auditoría para seguimiento de actividades
3. **RNF14**: Internacionalización con soporte para español colombiano

## Equipo de Desarrollo
- Homero Cabrera Araque


## Licencia
Este proyecto está desarrollado para fines académicos y no debe utilizarse en entornos de producción sin las debidas adaptaciones y pruebas.

© [Año] Universidad Politécnico Colombiano Jaime Isaza Cadavid - Todos los derechos reservados
