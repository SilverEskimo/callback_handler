import jwt
import helpers
import settings
from pathlib import Path
from logger_config import logger
from jwt import InvalidTokenError, ExpiredSignatureError, InvalidSignatureError, DecodeError
from typing import Callable, Awaitable
from fastapi import HTTPException, Request


def load_keys() -> tuple[str, str]:
    """Load and return the callback private key and cosigner public key."""
    try:
        with open(Path(settings.CALLBACK_PRIVATE_KEY_PATH), "r") as f1, \
             open(Path(settings.COSIGNER_PUBLIC_KEY_PATH), "r") as f2:
            return f1.read(), f2.read()
    except FileNotFoundError as e:
        logger.error(f"Could not load keys: {e}")
        raise


callback_private_key, cosigner_public_key = load_keys()
logger.info("Loaded callback private and cosigner public keys")


class JWTAuthenticator:
    def __init__(self):
        self._cosigner_public_key = cosigner_public_key
        self._callback_private_key = callback_private_key

    async def authenticate(self, request: Request) -> dict:
        try:
            body = await helpers.parse_body(request)
            return jwt.decode(body, self._cosigner_public_key, algorithms=["RS256"])
        except ExpiredSignatureError:
            logger.error("Token has expired.")
            raise HTTPException(status_code=401, detail="Token has expired.")
        except InvalidSignatureError:
            logger.error("Token signature is invalid.")
            raise HTTPException(status_code=403, detail="Token signature is invalid.")
        except DecodeError:
            logger.error("Token could not be decoded.")
            raise HTTPException(status_code=403, detail="Token could not be decoded.")
        except InvalidTokenError:
            logger.error("Invalid token.")
            raise HTTPException(status_code=403, detail="Invalid token.")

    def sign_response(self, response: dict) -> str:
        return jwt.encode(payload=response, key=self._callback_private_key, algorithm="RS256")


def authenticate_jwt(func: Callable[[Request, dict], Awaitable[dict]]):
    async def wrapper(request: Request) -> dict:
        authenticator = JWTAuthenticator()
        payload = await authenticator.authenticate(request)
        return await func(request, payload)
    return wrapper
