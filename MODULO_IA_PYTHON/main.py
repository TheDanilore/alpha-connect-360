from fastapi import FastAPI
from api import health

app = FastAPI(
    title='Alpha Connect - Microservicio IA',
    description='Servicios de IA para CRM de Odoo',
    version='0.1'
)

app.include_router(health.router)
