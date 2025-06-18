"""Custom exceptions for the SemaWal library."""

class SemaWalError(Exception):
    """Base class for exceptions in the SemaWal library."""
    pass

class NodeCreationError(SemaWalError):
    """Raised when an error occurs during node creation."""
    pass

class LinkError(SemaWalError):
    """Base class for errors related to links."""
    pass

class LinkCreationError(LinkError):
    """Raised when an error occurs during link creation."""
    pass

class NodeTypeConflictError(LinkError):
    """Raised when an operation is attempted with an incompatible node type."""
    pass

class PropertyError(SemaWalError):
    """Raised for errors related to node properties."""
    pass

class NetworkOperationError(SemaWalError):
    """Raised for errors during network operations."""
    pass

class NodeNotFoundError(NetworkOperationError):
    """Raised when a node is not found in the network."""
    pass
