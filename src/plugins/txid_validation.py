from src import settings
from typing import Dict, Any
from src.exceptions import PluginError
from src.plugins.interface import Plugin
from src.logs.logger_config import logger
from src.databases.mongo import MongoDB
from src.databases.postgres import PostgresDB


class TxidValidation(Plugin):
    async def process_request(self, data: Dict[str, Any]) -> bool:
        """Validates the transaction ID against the Database"""
        tx_id = data.get("txId")
        if tx_id is None:
            logger.error("Transaction ID (txId) is missing from the data.")
            raise PluginError("Transaction ID (txId) is missing.")
        try:
            result = await self._validate_txid(tx_id)
            logger.info(f"Approval result from TX ID Validation is: {result}")
            return result
        except PluginError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in TxID Validation plugin: {e}")
            raise PluginError(f"Unexpected error in TxID Validation plugin: {e}")

    async def _validate_txid(self, tx_id: str) -> bool:
        """Checks the database for the existence of a transaction ID."""
        logger.info(f"Validating that {tx_id} exists in the DB")
        await self.db.connect(**settings.DB_CONFIG)
        try:
            query, params = self._build_query(tx_id)
            result = await self.db.execute_query(query, *params)
            return bool(result)
        except RuntimeError:
            raise
        finally:
            await self.db.disconnect()

    def _build_query(self, tx_id: str) -> tuple:
        """Builds a query based on the database type."""
        query = ""
        params = ()
        if isinstance(self.db, PostgresDB):
            query = f"SELECT * FROM {settings.DB_TABLE} WHERE {settings.DB_COLUMN} = %s"
            params = (tx_id,)
        elif isinstance(self.db, MongoDB):
            query = {"find_one": {settings.DB_COLUMN: tx_id}}
        return query, params

    def __repr__(self) -> str:
        return "<Transaction ID Validation Plugin>"
