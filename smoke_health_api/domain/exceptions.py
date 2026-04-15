class DomainError(Exception):
    pass


class InvalidHealthStatusError(DomainError):
    pass


class InvalidServiceIdentityError(DomainError):
    pass


class HealthInvariantViolationError(DomainError):
    pass
