from loguru import logger


def log(message, level='INFO', indent=28):
    message = '\n'.join([' ' * indent + line for line in message.splitlines()])
    logger.log(
        level,
        message,
    )
