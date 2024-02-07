from typing import Optional
from dataclasses import dataclass
from src.authenticate import JWTAuthenticator
from src.logs.logger_config import logger


@dataclass
class CallbackResponse:
    action: str
    requestId: str
    rejectionReason: Optional[str] = None

    def get_response(self):
        return JWTAuthenticator().sign_response({
            "action": self.action,
            "requestId": self.requestId,
            "rejectionReason": self.rejectionReason,
        })