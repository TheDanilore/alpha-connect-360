# ========================================
# ALPHA CONNECT 360 - WINDOWS SETUP SCRIPT
# ========================================
# Script PowerShell para configurar y levantar el entorno

Write-Host "🚀 Iniciando configuración de Alpha Connect 360..." -ForegroundColor Green

# Función para mostrar mensajes con colores
function Write-AlphaMessage {
    param([string]$Message)
    Write-Host "[Alpha Connect] $Message" -ForegroundColor Green
}

function Write-AlphaWarning {
    param([string]$Message)
    Write-Host "[Warning] $Message" -ForegroundColor Yellow
}

function Write-AlphaError {
    param([string]$Message)
    Write-Host "[Error] $Message" -ForegroundColor Red
}

function Write-AlphaInfo {
    param([string]$Message)
    Write-Host "[Info] $Message" -ForegroundColor Blue
}

# Verificar si Docker Desktop está instalado
try {
    $dockerVersion = docker --version
    Write-AlphaMessage "✅ Docker está disponible: $dockerVersion"
} catch {
    Write-AlphaError "❌ Docker no está instalado. Por favor instala Docker Desktop para Windows."
    Write-Host "Descarga desde: https://www.docker.com/products/docker-desktop" -ForegroundColor Cyan
    exit 1
}

# Verificar Docker Compose
try {
    $composeVersion = docker-compose --version
    Write-AlphaMessage "✅ Docker Compose disponible: $composeVersion"
} catch {
    Write-AlphaError "❌ Docker Compose no está disponible."
    exit 1
}

# Verificar si Docker Desktop está corriendo
try {
    docker info | Out-Null
    Write-AlphaMessage "✅ Docker Desktop está corriendo"
} catch {
    Write-AlphaError "❌ Docker Desktop no está corriendo. Por favor inicia Docker Desktop."
    exit 1
}

# Crear directorios necesarios
Write-AlphaMessage "📁 Creando directorios necesarios..."
New-Item -ItemType Directory -Force -Path ".\logs" | Out-Null
New-Item -ItemType Directory -Force -Path ".\backups" | Out-Null
New-Item -ItemType Directory -Force -Path ".\filestore" | Out-Null

# Verificar si el puerto 8069 está disponible
$portCheck = netstat -an | Select-String ":8069"
if ($portCheck) {
    Write-AlphaWarning "⚠️ El puerto 8069 parece estar en uso:"
    Write-Host $portCheck -ForegroundColor Yellow
    $continue = Read-Host "¿Continuar de todos modos? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        exit 1
    }
}

# Construir las imágenes
Write-AlphaMessage "🔨 Construyendo imágenes Docker..."
try {
    docker-compose build
    Write-AlphaMessage "✅ Imágenes construidas exitosamente"
} catch {
    Write-AlphaError "❌ Error al construir las imágenes"
    exit 1
}

# Levantar PostgreSQL primero
Write-AlphaMessage "🐘 Iniciando PostgreSQL..."
docker-compose up -d postgres

# Esperar a que PostgreSQL esté listo
Write-AlphaMessage "⏳ Esperando a que PostgreSQL esté listo..."
Start-Sleep -Seconds 15

# Verificar si PostgreSQL está respondiendo
$maxAttempts = 10
$attempts = 0
do {
    try {
        $pgStatus = docker-compose exec -T postgres pg_isready -U odoo
        if ($pgStatus -like "*accepting connections*") {
            Write-AlphaMessage "✅ PostgreSQL está listo"
            break
        }
    } catch {
        # Continuar intentando
    }
    
    $attempts++
    Write-AlphaInfo "🔄 Intento $attempts de $maxAttempts..."
    Start-Sleep -Seconds 5
} while ($attempts -lt $maxAttempts)

if ($attempts -eq $maxAttempts) {
    Write-AlphaError "❌ PostgreSQL no respondió después de $maxAttempts intentos"
    Write-Host "Logs de PostgreSQL:" -ForegroundColor Yellow
    docker-compose logs postgres
    exit 1
}

# Verificar/crear base de datos
Write-AlphaInfo "🗄️ Verificando base de datos..."
try {
    $dbExists = docker-compose exec -T postgres psql -U odoo -lqt | Select-String "alpha_connect_db"
    if (-not $dbExists) {
        Write-AlphaMessage "🆕 Creando base de datos alpha_connect_db..."
        docker-compose exec -T postgres createdb -U odoo alpha_connect_db
    } else {
        Write-AlphaWarning "📊 La base de datos alpha_connect_db ya existe"
    }
} catch {
    Write-AlphaWarning "⚠️ No se pudo verificar la base de datos, continuando..."
}

# Levantar todos los servicios
Write-AlphaMessage "🚀 Iniciando todos los servicios..."
docker-compose up -d

# Esperar a que Odoo esté listo
Write-AlphaMessage "⏳ Esperando a que Odoo esté listo..."
Start-Sleep -Seconds 30

# Verificar estado de los servicios
Write-AlphaMessage "🔍 Verificando estado de los servicios..."
$services = docker-compose ps

if ($services -like "*Up*") {
    Write-AlphaMessage "✅ Servicios iniciados correctamente"
    
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "🎉 Alpha Connect 360 está listo!" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📊 Servicios disponibles:" -ForegroundColor White
    Write-Host "  • Odoo (CRM):     http://localhost:8069" -ForegroundColor Cyan
    Write-Host "  • PgAdmin:        http://localhost:5050" -ForegroundColor Cyan
    Write-Host "  • PostgreSQL:     localhost:5432" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🔐 Credenciales por defecto:" -ForegroundColor White
    Write-Host "  • Odoo Admin:     admin@alphaconnect.com / alpha_admin_2025" -ForegroundColor Yellow
    Write-Host "  • PgAdmin:        admin@alphaconnect.com / admin123" -ForegroundColor Yellow
    Write-Host "  • PostgreSQL:     odoo / odoo_password" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📝 Próximos pasos:" -ForegroundColor White
    Write-Host "  1. Abrir navegador en http://localhost:8069" -ForegroundColor Green
    Write-Host "  2. Crear base de datos 'alpha_connect_db'" -ForegroundColor Green
    Write-Host "  3. Instalar módulos: alpha_connect_theme, alpha_crm_extension" -ForegroundColor Green
    Write-Host ""
    Write-Host "🛠️ Comandos útiles:" -ForegroundColor White
    Write-Host "  • Ver logs:       docker-compose logs -f" -ForegroundColor Magenta
    Write-Host "  • Reiniciar:      docker-compose restart" -ForegroundColor Magenta
    Write-Host "  • Parar:          docker-compose down" -ForegroundColor Magenta
    Write-Host ""
    
    # Preguntar si abrir el navegador
    $openBrowser = Read-Host "¿Abrir Alpha Connect en el navegador? (Y/n)"
    if ($openBrowser -ne "n" -and $openBrowser -ne "N") {
        Start-Process "http://localhost:8069"
        Write-AlphaMessage "🌐 Abriendo Alpha Connect en el navegador..."
    }
    
} else {
    Write-AlphaError "❌ Error al iniciar los servicios"
    Write-Host ""
    Write-Host "📋 Estado de los contenedores:" -ForegroundColor Yellow
    docker-compose ps
    Write-Host ""
    Write-Host "📋 Logs de error:" -ForegroundColor Yellow
    docker-compose logs --tail=20
}

Write-Host ""
Write-Host "🔗 Para más información, consulta README.md" -ForegroundColor Cyan
Write-Host ""
