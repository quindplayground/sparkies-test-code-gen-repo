class DomainError(Exception):
    """Base type for domain-level failures."""


class InvalidHealthStatusError(DomainError):
    """Raised when a health status string violates domain invariants."""
