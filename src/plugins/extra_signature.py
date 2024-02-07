import base64
from src import settings
from src.exceptions import PluginError
from src.plugins.interface import Plugin
from src.logs.logger_config import logger
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key


class ExtraSignature(Plugin):
    def __init__(self, db_type: str):
        super().__init__(db_type)

    async def process_request(self, data: dict) -> bool:
        """Process the request by verifying the extra signature."""
        try:
            message = data.get("note")
            signature = data.get("extraParameters", {}).get("extraSignature")
            if not signature:
                raise PluginError("Missing extra signature")
            return await self._verify_signature(message, signature)
        except PluginError as e:
            logger.error(f"Failed to validate signature: {e}")
            raise

    @staticmethod
    async def _read_public_key() -> bytes:
        """Reads the public key from file."""
        try:
            with open(settings.EXTRA_SIGNATURE_PUBLIC_KEY_PATH, "rb") as f:
                return f.read()
        except FileNotFoundError as e:
            logger.error(f"Error reading public key file: {e}")
            raise PluginError(f"Error reading public key file: {e}")

    async def _verify_signature(self, string_to_sign: str, signature: str) -> bool:
        """Verifies the signature of the provided string."""
        try:
            public_key_bytes = await self._read_public_key()
            public_key = load_pem_public_key(public_key_bytes)
            signature_bytes = base64.b64decode(signature)
            public_key.verify(
                signature_bytes,
                string_to_sign.encode('utf-8'),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            logger.info("Signature verified successfully.")
            return True
        except Exception as e:
            logger.error(f"Error verifying signature: {e}")
            raise PluginError(f"Could not verify the extra signature: {e}")

    def _build_query(self):
        pass

    def __repr__(self) -> str:
        return "<Extra Signature validation Plugin>"
