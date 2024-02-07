import importlib
from src import settings
from typing import List, Type
from src.plugins.interface import Plugin
from src.databases.interface import DatabaseInterface
from src.exceptions import DatabaseUnsupportedError, PluginLoadError


class PluginManager:
    def __init__(self):
        self.plugins: List[Plugin] = []

    @staticmethod
    def _create_db_instance(db_type: str) -> DatabaseInterface:
        db_class = settings.DB_CLASS_MAP.get(db_type)
        if db_class is None:
            raise DatabaseUnsupportedError(f"Unsupported database type: {db_type}")
        return db_class()

    def _load_plugin(self, plugin_name: str, db_instance: DatabaseInterface):
        try:
            class_name = "".join(word.capitalize() for word in plugin_name.split("_"))
            module = importlib.import_module(f"src.plugins.{plugin_name}")
            plugin_class: Type[Plugin] = getattr(module, class_name)
            plugin_instance = plugin_class(db_instance)
            self.plugins.append(plugin_instance)
        except ImportError as e:
            raise PluginLoadError(f"Failed to import plugin {plugin_name}") from e
        except AttributeError as e:
            raise PluginLoadError(f"Plugin class missing in plugin {plugin_name}")
        except Exception:
            raise PluginLoadError(f"Unexpected error loading plugin {plugin_name}")

    def load_plugins(self, plugin_names: List[str], db_type: str):
        try:
            db_instance = self._create_db_instance(db_type)
            for plugin_name in plugin_names:
                self._load_plugin(plugin_name, db_instance)
        except PluginLoadError:
            raise

    def get_plugins(self) -> List[Plugin]:
        return self.plugins

    async def process_request(self, data: dict) -> bool:
        for plugin in self.plugins:
            if not await plugin.process_request(data):
                return False
        return True
