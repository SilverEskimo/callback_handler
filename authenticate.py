import jwt
import helpers
import settings
from pathlib import Path
from typing import Callable
from jwt import InvalidTokenError
from fastapi import HTTPException, Request
from logger_config import logger


private_key = Path(settings.CALLBACK_PRIVATE_KEY_PATH)
public_key = Path(settings.COSIGNER_PUBLIC_KEY_PATH)
cosigner_public_key = ""
callback_private_key = ""

try:
    with open(private_key, "r") as f1, open(public_key, "r") as f2:
        callback_private_key = f1.read()
        cosigner_public_key = f2.read()
        logger.info("Loaded callback private and cosigner public keys")
except FileNotFoundError as e:
    logger.error(f"Could not load keys: {e}")


class JWTAuthenticator:
    @staticmethod
    async def authenticate(request: Request):
        try:
            body = await helpers.parse_body(request)
            payload = jwt.decode(body, cosigner_public_key, algorithms=["RS256"])
            return payload
        except (InvalidTokenError, ValueError):
            raise HTTPException(status_code=403, detail="Authentication Failed")

    @staticmethod
    def sign_response(response):
        return jwt.encode(payload=response, key=callback_private_key, algorithm="RS256")


def authenticate_jwt(func: Callable):
    async def wrapper(request: Request):
        payload = await JWTAuthenticator().authenticate(request)
        return await func(payload)

    return wrapper
