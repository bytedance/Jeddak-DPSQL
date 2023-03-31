import enum


class MetaStatus(enum.Enum):
    """
        1: meta gen finished
        0: meta deleted
        2: meta is being generated
        -1: meta gen failed
    """
    FINISHED = 1
    DELETED = 0
    GENERATING = 2
    FAILED = -1
