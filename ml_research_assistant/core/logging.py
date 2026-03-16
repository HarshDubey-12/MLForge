"""Central logging setup used by all modules."""

import logging


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced application logger."""
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(name)

