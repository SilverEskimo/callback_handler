import base64
from src import settings
from src.exceptions import PluginError
from src.interfaces import Plugin
from src.logger_config import logger
from fastapi import HTTPException
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key


class ExtraSignature(Plugin):

    def __init__(self, db_type):
        super().__init__(db_type)

    async def process_request(self, data):
        try:
            message = data.get("note")
            signature = data.get("extraParameters").get("extraSignature")
            return await self._verify_signature(message, signature)
        except Exception as e:
            logger.error(f"Failed to validate signature: {e}")
            raise PluginError(f"Error in ExtraSignature plugin: {e}")


    @staticmethod
    async def _read_public_key():
        try:
            with open(settings.EXTRA_SIGNATURE_PUBLIC_KEY_PATH, "rb") as f:
                public_key_bytes = f.read()
            return public_key_bytes
        except Exception as e:
            logger.error(f"Error reading public key file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error reading public key file: {str(e)}")

    async def _verify_signature(self, string_to_sign: str, signature: str):
        try:
            public_key_bytes = await self._read_public_key()
            pem_format = public_key_bytes.decode('utf-8')
            public_key_obj = load_pem_public_key(pem_format.encode('utf-8'), backend=default_backend())
            signature_bytes = base64.b64decode(signature)
            public_key_obj.verify(
                signature_bytes,
                string_to_sign.encode('utf-8'),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            logger.info("Approval result from Extra Signature Validation is: True")
            return False
        except Exception as e:
            logger.error(f"Error verifying signature: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Could not verify the extra signature, error: {str(e)}")

    def _build_query(self):
        pass

    def __repr__(self):
        return "ExtraSignature"
