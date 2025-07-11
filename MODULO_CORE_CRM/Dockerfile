# Dockerfile para Odoo 18.0 personalizado para Alpha Connect
FROM python:3.11-slim-bullseye

# Configurar variables de entorno
ENV ODOO_VERSION=18.0
ENV ODOO_USER=odoo
ENV ODOO_HOME=/opt/odoo

# Crear usuario odoo
RUN useradd --create-home --home-dir $ODOO_HOME --no-log-init --shell /bin/bash $ODOO_USER

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    dirmngr \
    fonts-noto-cjk \
    gnupg \
    libssl-dev \
    node-less \
    npm \
    python3-num2words \
    python3-pdfminer \
    python3-pip \
    python3-phonenumbers \
    python3-pyldap \
    python3-qrcode \
    python3-renderpm \
    python3-setuptools \
    python3-slugify \
    python3-vobject \
    python3-watchdog \
    python3-xlrd \
    python3-xlwt \
    xz-utils \
    postgresql-client \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    libevent-dev \
    libsasl2-dev \
    libldap2-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar rtlcss para soporte RTL
RUN npm install -g rtlcss

# Crear directorio de configuración
RUN mkdir -p /etc/odoo

# Copiar Odoo al contenedor (como root para poder leer)
COPY ./odoo /opt/odoo

# Copiar configuración
COPY ./config/odoo.conf /etc/odoo/odoo.conf

# Crear directorio de datos
RUN mkdir -p /var/lib/odoo

# Instalar dependencias de Python
RUN pip3 install --no-cache-dir -r /opt/odoo/requirements.txt

# Cambiar propietario de archivos
RUN chown -R odoo:odoo /opt/odoo && chown -R odoo:odoo /etc/odoo && chown -R odoo:odoo /var/lib/odoo

# Cambiar al usuario odoo
USER $ODOO_USER

# Configurar variables de entorno para Odoo
ENV PATH="$ODOO_HOME:$PATH"

# Exponer puerto
EXPOSE 8069

# Directorio de trabajo
WORKDIR $ODOO_HOME

# Comando por defecto
CMD ["python3", "odoo-bin", "-c", "/etc/odoo/odoo.conf"]
