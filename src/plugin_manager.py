import importlib
from src.logger_config import logger
from src.databases.mongo import MongoDB
from src.databases.postgres import PostgresDB


class PluginManager:
    def __init__(self):
        self.plugins = []

    def load_plugins(self, plugin_names, db_type):

        if db_type == 'postgres':
            db_instance = PostgresDB()
        elif db_type == 'mongodb':
            db_instance = MongoDB()
        else:
            db_instance = None

        for plugin_name in plugin_names:
            try:
                class_name = "".join(
                    word.capitalize() for word in plugin_name.split("_")
                )
                module = importlib.import_module(name=f"src.plugins.{plugin_name}")
                plugin_class = getattr(module, class_name)
                plugin_instance = plugin_class(db_instance)
                self.plugins.append(plugin_instance)
            except Exception as e:
                logger.error(f"Failed to load plugin {plugin_name}: {e}")

    def get_plugins(self):
        return self.plugins

    async def process_request(self, data):
        for plugin in self.plugins:
            if not await plugin.process_request(data):
                return False

