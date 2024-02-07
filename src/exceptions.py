# In exceptions.py
class DatabaseConnectionError(Exception):
    """Exception raised when a database connection fails."""
    pass


class AuthenticationError(Exception):
    """Exception raised for errors in the authentication process."""
    pass


class PluginError(Exception):
    """Exception raised for errors within plugin operations."""
    pass


class ValidationError(Exception):
    """Exception raised for data validation errors."""
    pass


class DatabaseUnsupportedError(Exception):
    """Exception raised when an unsupported database type is specified."""
    pass


class PluginLoadError(Exception):
    """Exception raised when loading a plugin fails."""
    pass
