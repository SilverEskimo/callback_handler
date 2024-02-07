from src import settings
from src.exceptions import PluginError
from src.interfaces import Plugin
from src.logger_config import logger
from src.databases.mongo import MongoDB
from src.databases.postgres import PostgresDB


class TxidValidation(Plugin):
    async def process_request(self, data: dict) -> bool:
        try:
            tx_id = data.get("txId")
            result = await self._validate_txid(tx_id)
            logger.info(f"Approval result from TX ID Validation is: {result}")
            return result
        except Exception as e:
            raise PluginError(f"Error in TxID Validation plugin: {e}")

    async def _validate_txid(self, tx_id: str) -> bool:
        logger.info(f"Validating that {tx_id} exists in the DB")
        await self.db.connect(**settings.DB_CONFIG)
        try:
            query, params = self._build_query(tx_id)
            result = await self.db.execute_query(query, *params)
            return bool(result)
        finally:
            await self.db.disconnect()

    def _build_query(self, tx_id: str) -> tuple:
        params = (tx_id,)
        if isinstance(self.db, PostgresDB):
            query = f'SELECT * FROM {settings.DB_TABLE} ' \
                    f'WHERE {settings.DB_COLUMN} = $1'
            return query, params
        elif isinstance(self.db, MongoDB):
            query = { settings.DB_COLUMN: tx_id }
            return query, ("find_one",)
        else:
            raise NotImplementedError("Query generation not implemented for this database type")

    def __repr__(self) -> str:
        return "TxidValidation"

