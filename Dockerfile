FROM python:3.11-slim-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    build-essential \
    libxslt1-dev \
    libzip-dev \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    node-less \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Create odoo user
RUN useradd -ms /bin/bash odoo

# Set working directory
WORKDIR /opt/odoo

# Copy our complete modified Odoo source
COPY . /opt/odoo/

# Install Python dependencies
RUN pip install -r requirements.txt

# Set proper ownership
RUN chown -R odoo:odoo /opt/odoo

# Create necessary directories
RUN mkdir -p /var/lib/odoo && chown odoo:odoo /var/lib/odoo
RUN mkdir -p /etc/odoo && chown odoo:odoo /etc/odoo

# Switch to odoo user
USER odoo

# Expose port
EXPOSE 8069

# Set entrypoint
CMD ["python3", "/opt/odoo/odoo-bin", "-c", "/etc/odoo/odoo.conf"]
