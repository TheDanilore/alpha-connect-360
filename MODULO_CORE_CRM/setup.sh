#!/bin/bash

# ========================================
# ALPHA CONNECT 360 - SETUP SCRIPT
# ========================================
# Script para configurar y levantar el entorno de desarrollo

echo "🚀 Iniciando configuración de Alpha Connect 360..."

# Colores para los mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
print_message() {
    echo -e "${GREEN}[Alpha Connect]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[Warning]${NC} $1"
}

print_error() {
    echo -e "${RED}[Error]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[Info]${NC} $1"
}

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado. Por favor instala Docker Desktop."
    exit 1
fi

# Verificar si Docker Compose está disponible
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_error "Docker Compose no está disponible."
    exit 1
fi

print_message "✅ Docker está disponible"

# Crear directorios necesarios si no existen
print_message "📁 Creando directorios necesarios..."
mkdir -p ./logs
mkdir -p ./backups
mkdir -p ./filestore

# Configurar permisos para Odoo
print_message "🔐 Configurando permisos..."
chmod -R 755 ./custom_addons
chmod -R 755 ./config

# Construir las imágenes
print_message "🔨 Construyendo imágenes Docker..."
docker-compose build

# Verificar si ya existe una base de datos
print_info "🗄️ Verificando estado de la base de datos..."

# Levantar solo PostgreSQL primero
print_message "🐘 Iniciando PostgreSQL..."
docker-compose up -d postgres

# Esperar a que PostgreSQL esté listo
print_message "⏳ Esperando a que PostgreSQL esté listo..."
sleep 10

# Verificar si la base de datos alpha_connect_db existe
DB_EXISTS=$(docker-compose exec -T postgres psql -U odoo -lqt | cut -d \| -f 1 | grep -qw alpha_connect_db && echo "true" || echo "false")

if [ "$DB_EXISTS" = "false" ]; then
    print_message "🆕 Creando nueva base de datos alpha_connect_db..."
    docker-compose exec -T postgres createdb -U odoo alpha_connect_db
else
    print_warning "📊 La base de datos alpha_connect_db ya existe"
fi

# Levantar todos los servicios
print_message "🚀 Iniciando todos los servicios..."
docker-compose up -d

# Esperar a que Odoo esté listo
print_message "⏳ Esperando a que Odoo esté listo..."
sleep 30

# Verificar si los servicios están corriendo
print_message "🔍 Verificando estado de los servicios..."

if docker-compose ps | grep -q "Up"; then
    print_message "✅ Servicios iniciados correctamente"
    
    echo ""
    echo "=========================================="
    echo "🎉 Alpha Connect 360 está listo!"
    echo "=========================================="
    echo ""
    echo "📊 Servicios disponibles:"
    echo "  • Odoo (CRM):     http://localhost:8069"
    echo "  • PgAdmin:        http://localhost:5050"
    echo "  • PostgreSQL:     localhost:5432"
    echo ""
    echo "🔐 Credenciales por defecto:"
    echo "  • Odoo Admin:     admin / admin"
    echo "  • PgAdmin:        admin@alphaconnect.com / admin123"
    echo "  • PostgreSQL:     odoo / odoo_password"
    echo ""
    echo "📝 Notas importantes:"
    echo "  • Primera vez: Crear base de datos 'alpha_connect_db'"
    echo "  • Instalar módulos: alpha_connect_theme, alpha_crm_extension"
    echo "  • Los logs están en ./logs/"
    echo ""
    echo "🛠️ Comandos útiles:"
    echo "  • Ver logs:       docker-compose logs -f"
    echo "  • Reiniciar:      docker-compose restart"
    echo "  • Parar:          docker-compose down"
    echo "  • Update apps:    docker-compose restart odoo"
    echo ""
    
else
    print_error "❌ Error al iniciar los servicios"
    echo "📋 Estado de los contenedores:"
    docker-compose ps
    echo ""
    echo "📋 Logs de error:"
    docker-compose logs --tail=20
fi
