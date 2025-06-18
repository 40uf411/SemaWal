"""
SemaWal: A Semantic Network Library
"""

# Import core classes
from .node import Node
from .net import Net

# Import custom exceptions
from .exceptions import (
    SemaWalError,
    NodeCreationError,
    LinkError,
    LinkCreationError,
    NodeTypeConflictError,
    PropertyError,
    NetworkOperationError,
    NodeNotFoundError
)

# Define what is available for `from semawal import *`
__all__ = [
    'Node',
    'Net',
    'SemaWalError',
    'NodeCreationError',
    'LinkError',
    'LinkCreationError',
    'NodeTypeConflictError',
    'PropertyError',
    'NetworkOperationError',
    'NodeNotFoundError'
]
