from fastapi import APIRouter, Header, HTTPException
from core.config import API_KEY

router = APIRouter()

@router.get('/healthcheck')
def healthcheck(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return {'status': 'ok', 'message': 'IA service running'}
