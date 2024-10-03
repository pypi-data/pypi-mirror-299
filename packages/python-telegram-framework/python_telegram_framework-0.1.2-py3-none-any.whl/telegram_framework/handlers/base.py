from importlib import import_module

from telegram_framework.conf import settings

def include(arg, abspath=False):
    """Includes handlers defined in another module.
    
    Args:
        arg (str): Path to the handlers module. It can be relative to the directory configured for the modules in settings.py, or absolute from the root of the project.
        abspath (bool): If True, `arg` is considered an absolute path from the project root.

    Returns:
        list: List of handlers included from the specified module
    """
    try:
        if not abspath:
            arg = f"{settings.MODULES_DIR}.{arg}" #TODO: arreglaro, por algun motivo no lee la variable de entorno de los settings
        handler_module = import_module(arg)
        handlers = getattr(handler_module, 'handlers')
    except ModuleNotFoundError:
        print(f"The module {arg} does not exist")
    except AttributeError:
        print(f"The module {arg} does not have a 'handlers' attribute")
    
    return handlers
