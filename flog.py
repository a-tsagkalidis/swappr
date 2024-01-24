from loguru import logger


def log(message, level='INFO', indent=28):
    message = '\n'.join([' ' * indent + line for line in message.splitlines()])
    logger.log(
        level,
        message,
    )


def initialize_logger():
    logger.add(
        'app.log',
        format="{level}:swappr:[{time:DD/MMM/YYYY HH:mm:ss}]: {message}",
        colorize=True,
        backtrace=True,
        diagnose=True
    )
