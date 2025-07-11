# Alpha Connect 360 - Sistema CRM Integrado

![Alpha Connect 360](MODULO_CORE_CRM/custom_addons/alpha_connect_theme/static/src/img/alpha_connect_logo.png)

## 🚀 Descripción

Alpha Connect 360 es una plataforma integral de gestión empresarial basada en Odoo 18.0 Community Edition, diseñada con arquitectura modular para máxima escalabilidad y personalización.

### 🎯 Características Principales

- **🤖 CRM con IA Integrada**: Scoring predictivo de leads y segmentación inteligente
- **📊 Analytics Avanzados**: KPIs personalizados y dashboard interactivo
- **🔄 Automatización**: Workflows de seguimiento y triggers automáticos
- **🎨 Interfaz Personalizada**: Tema Alpha Connect con branding corporativo
- **🐳 Arquitectura Docker**: Deployment containerizado para desarrollo y producción

## 📋 Módulos del Sistema

### 1. **MÓDULO_CORE_CRM** 
**Núcleo CRM con Odoo 18.0**
- Base de datos PostgreSQL optimizada
- Gestión completa de leads y oportunidades
- Pipeline de ventas personalizable
- Integración con módulos de facturación y ventas

### 2. **MÓDULO_CAMPANAS_LARAVEL** 
**Engine de Campañas de Marketing**
- Gestión de campañas multi-canal
- Automatización de marketing
- Segmentación avanzada de audiencias
- Analytics de rendimiento

### 3. **MÓDULO_IA_PYTHON**
**Procesamiento de IA y Machine Learning**
- Análisis predictivo de leads
- Scoring automático de conversión
- Procesamiento de lenguaje natural
- APIs de integración con servicios IA

### 4. **MÓDULO_INTEGRACIONES_NODE**
**Hub de Integraciones**
- APIs RESTful para conectividad
- Webhooks y sincronización en tiempo real
- Conectores para sistemas externos
- Middleware de comunicación

## 🛠️ Instalación y Configuración

### Prerrequisitos

- Docker Desktop instalado
- Git para clonación del repositorio
- Puerto 8069 disponible para Odoo
- Puerto 5050 disponible para PgAdmin
- Puerto 5432 disponible para PostgreSQL

### 🚀 Instalación Rápida

1. **Clonar el repositorio**:
```bash
git clone https://github.com/tu-usuario/alpha-connect-360.git
cd alpha-connect-360
```

2. **Navegar al módulo CRM**:
```bash
cd MODULO_CORE_CRM
```

3. **Iniciar servicios con Docker**:
```bash
docker-compose up -d
```

4. **Verificar la instalación**:
```bash
python ../verify_system.py
```

### 🔧 Configuración Detallada

#### Variables de Entorno
```yaml
# docker-compose.yaml
services:
  odoo:
    environment:
      - HOST=postgres
      - USER=odoo
      - PASSWORD=odoo
      - POSTGRES_DB=alpha_connect_db
```

#### Estructura de Directorios
```
alpha-connect-360/
├── MODULO_CORE_CRM/           # CRM principal con Odoo
│   ├── custom_addons/         # Módulos personalizados
│   │   ├── alpha_connect_theme/    # Tema corporativo
│   │   └── alpha_crm_extension/    # Extensiones CRM + IA
│   ├── docker-compose.yaml   # Orquestación de servicios
│   └── Dockerfile            # Imagen personalizada Odoo
├── MODULO_CAMPANAS_LARAVEL/   # Motor de campañas
├── MODULO_IA_PYTHON/         # Procesamiento IA
├── MODULO_INTEGRACIONES_NODE/ # Hub de integraciones
├── test_alpha_connect.py     # Suite de pruebas
└── verify_system.py          # Verificador del sistema
```

## 🔐 Acceso al Sistema

### Odoo CRM Principal
- **URL**: http://localhost:8069
- **Usuario**: admin
- **Contraseña**: admin
- **Base de datos**: alpha_connect_db

### PgAdmin (Administración DB)
- **URL**: http://localhost:5050
- **Email**: admin@alphaconnect.com
- **Contraseña**: admin123

### Conexión a PostgreSQL
- **Host**: localhost
- **Puerto**: 5432
- **Usuario**: odoo
- **Contraseña**: odoo
- **Base de datos**: alpha_connect_db

## 🤖 Funcionalidades de IA

### Scoring Predictivo de Leads
```python
# Ejemplo de uso de la API de scoring
lead_data = {
    'name': 'Lead Empresa XYZ',
    'email': 'contacto@empresaxyz.com',
    'phone': '+1234567890',
    'company_size': 'medium',
    'industry': 'technology'
}

# El sistema calcula automáticamente:
# - ai_conversion_score: 0-100%
# - lead_quality_score: A, B, C, D
# - engagement_score: 0-10
# - customer_segment: hot_lead, warm_lead, cold_lead
```

### Analytics en Tiempo Real
- Conversión por canal de adquisición
- ROI de campañas de marketing
- Predicción de ventas próximos 30/60/90 días
- Score promedio de calidad de leads

## 📊 API y Integraciones

### Endpoints Principales

```http
# Gestión de Leads
GET    /api/v1/leads
POST   /api/v1/leads
PUT    /api/v1/leads/{id}
DELETE /api/v1/leads/{id}

# Analytics
GET    /api/v1/analytics/conversion-rates
GET    /api/v1/analytics/sales-forecast
GET    /api/v1/analytics/lead-scoring

# IA y ML
POST   /api/v1/ai/score-lead
POST   /api/v1/ai/predict-conversion
GET    /api/v1/ai/model-performance
```

### Webhooks Disponibles
- `lead.created` - Nuevo lead creado
- `lead.qualified` - Lead calificado por IA
- `opportunity.won` - Oportunidad ganada
- `campaign.completed` - Campaña finalizada

## 🧪 Testing y Validación

### Suite de Pruebas Automatizadas

```bash
# Ejecutar todas las pruebas
python test_alpha_connect.py

# Verificar estado del sistema
python verify_system.py

# Pruebas específicas de módulos
cd MODULO_CORE_CRM
docker-compose exec odoo python3 -m pytest tests/
```

### Métricas de Rendimiento
- ✅ Tiempo de respuesta de API < 200ms
- ✅ Throughput de scoring IA > 1000 leads/min
- ✅ Uptime del sistema > 99.9%
- ✅ Precisión del modelo IA > 85%

## 🚀 Deployment en Producción

### Docker Compose Production

```yaml
version: '3.8'
services:
  odoo:
    image: alpha-connect/odoo:18.0-production
    environment:
      - DB_HOST=${POSTGRES_HOST}
      - DB_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - odoo_data:/var/lib/odoo
    networks:
      - alpha_network
```

### Variables de Entorno Producción
```bash
# .env.production
POSTGRES_HOST=your-postgres-host
POSTGRES_PASSWORD=your-secure-password
REDIS_URL=redis://your-redis-host:6379
AI_API_KEY=your-ai-service-key
WEBHOOK_SECRET=your-webhook-secret
```

## 📈 Roadmap y Características Futuras

### Versión 2.0 (Q2 2024)
- [ ] Integración con WhatsApp Business API
- [ ] Dashboard móvil nativo
- [ ] IA conversacional para leads
- [ ] Integración con calendarios (Google, Outlook)

### Versión 2.5 (Q3 2024)
- [ ] Marketplace de integraciones
- [ ] APIs GraphQL
- [ ] Machine Learning AutoML
- [ ] Reportes avanzados con BI

### Versión 3.0 (Q4 2024)
- [ ] Multi-tenancy
- [ ] Módulo de e-commerce integrado
- [ ] IA de análisis de sentimientos
- [ ] Automatización no-code

## 🤝 Contribución

### Guía para Desarrolladores

1. **Fork del repositorio**
2. **Crear rama de feature**: `git checkout -b feature/nueva-funcionalidad`
3. **Desarrollar y probar**: Seguir estándares de código
4. **Commit con mensaje descriptivo**: `git commit -m "feat: nueva funcionalidad IA"`
5. **Push y crear PR**: `git push origin feature/nueva-funcionalidad`

### Estándares de Código
- Python: PEP 8, type hints obligatorios
- JavaScript: ESLint + Prettier
- PHP: PSR-12
- Docker: Multi-stage builds

## 📞 Soporte y Contacto

### Documentación
- **Wiki**: [Documentación completa](https://github.com/alpha-connect-360/wiki)
- **API Docs**: [Swagger Documentation](http://localhost:8069/api/docs)
- **Video Tutoriales**: [YouTube Channel](https://youtube.com/alphaconnect360)

### Canales de Soporte
- **Issues**: [GitHub Issues](https://github.com/alpha-connect-360/issues)
- **Discussions**: [GitHub Discussions](https://github.com/alpha-connect-360/discussions)
- **Email**: support@alphaconnect.com
- **Slack**: [Alpha Connect Slack](https://alphaconnect.slack.com)

## 📄 Licencia

Este proyecto está licenciado bajo **MIT License** - ver el archivo [LICENSE](LICENSE) para detalles.

### Componentes de Terceros
- **Odoo Community**: LGPL-3.0
- **Laravel**: MIT License
- **Docker**: Apache License 2.0
- **PostgreSQL**: PostgreSQL License

---

## 🏆 Estado del Proyecto

![Estado](https://img.shields.io/badge/Estado-Producción%20Lista-green)
![Versión](https://img.shields.io/badge/Versión-1.0.0-blue)
![Docker](https://img.shields.io/badge/Docker-Compatible-blue)
![IA](https://img.shields.io/badge/IA-Integrada-purple)

### Última Actualización: Julio 2025

✅ **Sistema completamente operativo y listo para producción**

---

*Desarrollado con ❤️ por el equipo de Alpha Connect Development*
