# 🚀 Alpha Connect 360 - Core CRM Module

![Alpha Connect Logo](./custom_addons/alpha_connect_theme/static/src/img/alpha_connect_logo.png)

## 📋 Descripción

Alpha Connect 360 es una plataforma CRM personalizada basada en Odoo 18.0 Community, diseñada específicamente para empresas que requieren funcionalidades avanzadas de IA predictiva, segmentación inteligente de clientes y automatización de procesos comerciales.

## 🎯 Características Principales

### 🤖 IA Predictiva y Generativa (Alpha Predict)
- **Scoring de Conversión**: Análisis automático de probabilidad de conversión de leads
- **Segmentación Inteligente**: Clasificación automática de clientes y prospects
- **Recomendaciones Personalizadas**: Sugerencias de acciones basadas en IA
- **Análisis de Comportamiento**: Evaluación de engagement y patrones de compra

### 🎨 Interfaz Personalizada Alpha Connect
- **Branding Completo**: Logos, colores y tipografía Alpha Connect
- **UI/UX Optimizada**: Diseño moderno y responsivo
- **Dashboard Interactivo**: Métricas en tiempo real con visualizaciones avanzadas
- **Tema Personalizado**: Eliminación completa de referencias a Odoo

### 📊 CRM Extendido
- **Pipeline Personalizado**: Etapas optimizadas para Alpha Connect
- **Campos IA**: Scoring, segmentación y análisis predictivo
- **Automatización**: Workflows inteligentes y triggers automáticos
- **Analytics Avanzados**: KPIs y métricas personalizadas

## 🏗️ Arquitectura del Sistema

```
ALPHA CONNECT 360
│
├── 🏢 MODULO_CORE_CRM (Odoo 18.0)
│   ├── 🐘 PostgreSQL Database
│   ├── 🔧 Custom Addons
│   │   ├── alpha_connect_theme/     # Personalización visual
│   │   └── alpha_crm_extension/     # Extensiones CRM + IA
│   └── 🐳 Docker Container
│
├── 🤖 MODULO_IA_PYTHON (FastAPI)
│   ├── 📊 Modelos ML/AI
│   ├── 🔄 APIs de Predicción
│   └── 📈 Analytics Engine
│
├── 🎯 MODULO_CAMPANAS_LARAVEL
│   ├── 📧 Campaign Management
│   ├── 🎨 Visual Builder
│   └── 🔄 Automation Engine
│
└── 🔗 MODULO_INTEGRACIONES_NODE
    ├── 🎫 PassCreator Integration
    ├── 🏢 HiOffice Connector
    └── 📱 External APIs
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- **Docker Desktop** (Windows/Mac) o **Docker Engine** (Linux)
- **Docker Compose** v2.0+
- **Git** para clonar el repositorio
- **8GB RAM** mínimo recomendado
- **Puertos disponibles**: 8069, 5432, 5050

### 1. Clonar el Repositorio

```bash
git clone https://github.com/your-organization/alpha-connect-360.git
cd alpha-connect-360/MODULO_CORE_CRM
```

### 2. Configuración Inicial

#### Para Windows (PowerShell):
```powershell
# Dar permisos al script
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Ejecutar setup
./setup.ps1
```

#### Para Linux/Mac:
```bash
# Dar permisos de ejecución
chmod +x setup.sh

# Ejecutar setup
./setup.sh
```

### 3. Configuración Manual (si prefieres)

```bash
# 1. Construir las imágenes
docker-compose build

# 2. Levantar servicios
docker-compose up -d

# 3. Verificar estado
docker-compose ps
```

## 🔧 Configuración Post-Instalación

### 1. Acceso Inicial

1. **Abrir navegador**: `http://localhost:8069`
2. **Crear base de datos**:
   - Database Name: `alpha_connect_db`
   - Email: `admin@alphaconnect.com`
   - Password: `alpha_admin_2025`
   - Phone: `+1234567890`
   - Language: `Spanish / Español`
   - Country: `Ecuador` (o tu país)

### 2. Instalación de Módulos

1. **Ir a Apps** (Aplicaciones)
2. **Buscar e instalar** en orden:
   - `alpha_connect_theme` (Tema Alpha Connect)
   - `alpha_crm_extension` (CRM Extensions)
   - `crm` (CRM base de Odoo)
   - `sale` (Ventas)
   - `mail` (Email)

### 3. Configuración de Pipeline

Los stages del CRM se crean automáticamente:
- 🆕 **Nuevo Lead** (10% probabilidad)
- 🔍 **Calificación** (25% probabilidad)
- 🎯 **Demo/Presentación** (50% probabilidad)
- 📋 **Propuesta** (70% probabilidad)
- 🤝 **Negociación** (85% probabilidad)
- ✅ **Ganado** (100% probabilidad)
- ❌ **Perdido** (0% probabilidad)
- 🌱 **Nurturing** (15% probabilidad)

## 📊 Funcionalidades Principales

### 🤖 Análisis de IA

#### En Leads/Oportunidades:
- **Botón "🤖 AI Analysis"**: Ejecuta análisis completo del lead
- **AI Conversion Score**: Score de 0-100% de probabilidad de conversión
- **Customer Segment**: Segmentación automática (Hot/Warm/Cold Lead)
- **Quality Score**: Evaluación basada en múltiples factores
- **Engagement Score**: Medición de interacciones digitales

#### En Clientes:
- **Customer Lifetime Value (CLV)**: Valor proyectado del cliente
- **Churn Risk Score**: Probabilidad de abandono
- **Customer Segment**: Clasificación (VIP, Loyal, At Risk, etc.)
- **Next Best Action**: Siguiente acción recomendada

### 📈 Campos Extendidos

#### Para Leads:
```
🔍 Acquisition Channel      📊 Industry Sector
📏 Company Size            💰 Annual Revenue Range
⚡ Urgency Level          ⏰ Decision Timeline
🌐 Website Sessions        📧 Email Engagement
📱 Social Engagement       🎯 Competitive Analysis
```

#### Para Customers:
```
💎 Loyalty Points          🏆 Loyalty Tier
🛒 Purchase Frequency      📊 Average Order Value
📞 Preferred Communication 🌐 Social Media Profiles
🏢 Company Information     📈 Behavioral Analytics
```

## 🔗 Servicios Disponibles

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| **Odoo CRM** | http://localhost:8069 | admin@alphaconnect.com / alpha_admin_2025 |
| **PgAdmin** | http://localhost:5050 | admin@alphaconnect.com / admin123 |
| **PostgreSQL** | localhost:5432 | odoo / odoo_password |

## 🛠️ Comandos Útiles

### Docker Management
```bash
# Ver logs en tiempo real
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Parar todos los servicios
docker-compose down

# Rebuild y restart
docker-compose down && docker-compose build && docker-compose up -d

# Limpiar volúmenes (⚠️ Borra datos)
docker-compose down -v
```

### Odoo Management
```bash
# Ejecutar shell de Odoo
docker-compose exec odoo odoo shell -d alpha_connect_db

# Update de módulos
docker-compose exec odoo odoo -d alpha_connect_db -u alpha_connect_theme,alpha_crm_extension

# Backup de base de datos
docker-compose exec postgres pg_dump -U odoo alpha_connect_db > backup_$(date +%Y%m%d).sql
```

## 📁 Estructura de Archivos

```
MODULO_CORE_CRM/
├── 📄 docker-compose.yml          # Orquestación de servicios
├── 📄 Dockerfile                  # Imagen personalizada de Odoo
├── 📄 setup.sh                    # Script de instalación
├── 📁 config/
│   └── 📄 odoo.conf              # Configuración de Odoo
├── 📁 odoo/                      # Código fuente de Odoo 18.0
├── 📁 custom_addons/
│   ├── 📁 alpha_connect_theme/    # Personalización visual
│   │   ├── 📁 static/src/
│   │   │   ├── 📁 css/           # Estilos personalizados
│   │   │   ├── 📁 js/            # JavaScript customizado
│   │   │   └── 📁 img/           # Logos y assets
│   │   ├── 📁 views/             # Templates XML
│   │   └── 📁 data/              # Configuraciones
│   └── 📁 alpha_crm_extension/   # Extensiones CRM
│       ├── 📁 models/            # Modelos extendidos
│       ├── 📁 views/             # Vistas personalizadas
│       ├── 📁 data/              # Datos iniciales
│       └── 📁 security/          # Permisos
├── 📁 logs/                      # Logs del sistema
└── 📁 backups/                   # Backups automáticos
```

## 🔍 Troubleshooting

### Problemas Comunes

#### 1. Puerto 8069 en uso
```bash
# Windows
netstat -ano | findstr :8069
taskkill /PID <PID> /F

# Linux/Mac
sudo lsof -i :8069
sudo kill -9 <PID>
```

#### 2. Error de permisos
```bash
# Linux/Mac
sudo chown -R $USER:$USER ./custom_addons
chmod -R 755 ./custom_addons
```

#### 3. Base de datos corrupta
```bash
# Resetear completamente
docker-compose down -v
docker-compose up -d
```

#### 4. Módulos no aparecen
```bash
# Restart Odoo en modo developer
docker-compose restart odoo
# Luego ir a Settings > Developer Tools > Update Apps List
```

### Logs de Debug

```bash
# Ver logs específicos
docker-compose logs postgres  # Logs de base de datos
docker-compose logs odoo      # Logs de Odoo
docker-compose logs pgadmin   # Logs de PgAdmin

# Logs con timestamp
docker-compose logs -t -f
```

## 🚀 Roadmap de Desarrollo

### ✅ Fase 1: Configuración Base (Actual)
- [x] Docker environment
- [x] Odoo 18.0 setup
- [x] Custom theme
- [x] Extended CRM models
- [x] Basic AI fields

### 🔄 Fase 2: Módulo IA Python (En desarrollo)
- [ ] FastAPI microservice
- [ ] ML models (Scoring, Segmentation)
- [ ] Integration endpoints
- [ ] Real-time predictions

### 📋 Fase 3: Frontend React
- [ ] Modern dashboard
- [ ] Interactive charts
- [ ] Real-time updates
- [ ] Mobile responsive

### 🎯 Fase 4: Campaign Orchestrator
- [ ] Laravel backend
- [ ] Visual campaign builder
- [ ] Automation engine
- [ ] A/B testing

### 🔗 Fase 5: External Integrations
- [ ] PassCreator connector
- [ ] HiOffice integration
- [ ] OAuth2 authentication
- [ ] Webhook handlers

## 👥 Equipo de Desarrollo

- **Lead Developer**: Alpha Connect Team
- **DevOps**: Docker & Infrastructure
- **Backend**: Python/FastAPI + Odoo
- **Frontend**: React + TailwindCSS
- **Mobile**: React Native (futuro)

## 📞 Soporte

- **Email**: dev@alphaconnect.com
- **Documentation**: `/docs` (futuro)
- **Issues**: GitHub Issues
- **Discord**: Alpha Connect Dev

## 📄 Licencia

Este proyecto está bajo licencia LGPL-3.0 para los componentes de Odoo y licencias propietarias para las extensiones Alpha Connect.

---

**🎉 ¡Felicidades! Alpha Connect 360 Core CRM está listo para usar.**

Para continuar con el desarrollo, revisa la documentación de cada módulo en sus respectivos directorios.
