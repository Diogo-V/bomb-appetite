import structlog

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(),
        structlog.processors.KeyValueRenderer(),
    ]
)

logger = structlog.get_logger()
