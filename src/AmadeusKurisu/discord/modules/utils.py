import logging
from os import listdir
from datetime import datetime
from discord.ext.commands import ExtensionError
from AmadeusKurisu import config

def generate_logger():
    logger = logging.getLogger("AmaKuri")
    logger.setLevel(logging.WARN)

    logger.addHandler(logging.StreamHandler())

    return logger

def populate_modules():
    moduleDirectory = config.MODULEPATH
    modules = listdir(moduleDirectory)

    # Format for later usage loading modules
    moduleDirectory = moduleDirectory.replace("./src/").replace("/", ".")

    return moduleDirectory, modules

_logger = generate_logger()
_moduleDirectory, _modules = populate_modules()


def _get_logger():
    return _logger

def get_modules():
    return _modules

def get_module_path():
    return _moduleDirectory

async def send_message(context, message):
    if context:
        await context.send(message)

async def load_module(client, module, context=None):
    logger = _get_logger()

    if context and context != "LOAD" and context not in config.bot["admin"]:
        logger.warning("Unauthorized user {} in {} attempted to call {} at {}.".format(
            context.author.display_name,
            context.guild.name,
            context.command,
            datetime.utcnow()))
        return False

    if context and context != "LOAD" and module not in _modules:
        logger.info("{} attempted to load invalid module {}.".format(
                    context.author.display_name,
                    module))
        await send_message(context, f"{module} is not a valid module.")
        return False

    if context == "LOAD" and module not in _modules:
        logger.critical(f"Attempted to load invalid module {module}.")
        return False

    try:
        client.load_extension(f"{_moduleDirectory}.{module}")
        logger.info(f"Loaded module {module}.")
        if context and context != "LOAD":
            await send_message(context, f"Module {module} loaded successfully.")
        return True
    except (AttributeError, ImportError, ExtensionError) as e:
        logger.warning(f"Failed to load module {module}.")
        logger.warning(f"{module}:{e}")
        if context and context != "LOAD":
            await send_message(context, f"Module {module} failed to load.")
        return False

async def unload_module(client, module, context=None):
    logger = _get_logger()

    if context and context != "UNLOAD" and context not in config.bot["admin"]:
        logger.warning("Unauthorized user {} in {} attempted to call {} at {}.".format(
            context.author.display_name,
            context.guild.name,
            context.command,
            datetime.utcnow()))
        return False

    try:
        client.unload_extension(f"{_moduleDirectory}.{module}")
        logger.info(f"Unloaded module {module}.")
        if context and context != "UNLOAD":
            await send_message(context, f"Module {module} unloaded successfully.")
        return True
    except (AttributeError, ImportError, ExtensionError) as e:
        logger.warning(f"Failed to unload module {module}.")
        logger.warning(f"{module}:{e}")
        if context and context != "UNLOAD":
            await send_message(context, f"Module {module} failed to unload.")
        return False
