FROM php:8.2-fpm-alpine

# === METADATOS ===
LABEL maintainer="Alpha Connect Development Team"
LABEL description="Laravel Microservice for Campaign Management"
LABEL version="1.0.0"

# === INSTALAR DEPENDENCIAS DEL SISTEMA ===
RUN apk add --no-cache \
    nginx \
    supervisor \
    curl \
    zip \
    unzip \
    git \
    mysql-client \
    libpng-dev \
    libjpeg-turbo-dev \
    freetype-dev \
    libzip-dev \
    icu-dev \
    oniguruma-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
        pdo_mysql \
        gd \
        zip \
        intl \
        mbstring \
        opcache

# === INSTALAR REDIS EXTENSION ===
RUN pecl install redis && docker-php-ext-enable redis

# === INSTALAR COMPOSER ===
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# === CONFIGURAR NGINX ===
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/default.conf /etc/nginx/conf.d/default.conf

# === CONFIGURAR SUPERVISOR ===
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# === CONFIGURAR PHP ===
COPY docker/php.ini /usr/local/etc/php/php.ini
COPY docker/php-fpm.conf /usr/local/etc/php-fpm.d/www.conf

# === CONFIGURAR DIRECTORIO DE TRABAJO ===
WORKDIR /var/www/html

# === COPIAR ARCHIVOS DE LARAVEL ===
COPY . .

# === INSTALAR DEPENDENCIAS DE COMPOSER ===
RUN composer install --optimize-autoloader --no-dev

# === CONFIGURAR PERMISOS ===
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html/storage \
    && chmod -R 755 /var/www/html/bootstrap/cache

# === CREAR DIRECTORIOS NECESARIOS ===
RUN mkdir -p /var/log/supervisor \
    && mkdir -p /run/nginx

# === EXPONER PUERTO ===
EXPOSE 80

# === COMANDO DE INICIO ===
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
