class TenantError(Exception):
    """Base class for all tenant-related errors."""
    pass


class TenantAlreadyExists(TenantError):
    """Raised when attempting to create a tenant that already exists."""
    pass


class TenantNotFound(TenantError):
    """Raised when a requested tenant cannot be found."""
    pass


class InvalidTenantPayload(TenantError):
    """Raised when tenant input data is invalid."""
    pass


class Unauthorized(TenantError):
    """Raised when an actor lacks permission to perform an action."""
    pass
