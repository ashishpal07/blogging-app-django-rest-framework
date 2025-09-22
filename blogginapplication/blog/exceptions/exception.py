# blog/services/exceptions.py
from rest_framework.exceptions import APIException
from rest_framework import status

class DomainError(Exception):
    code = "domain_error"
    message = "Domain error"
    http_status = status.HTTP_400_BAD_REQUEST

class NotFoundError(DomainError):
    code = "not_found"
    message = "Resource not found"
    http_status = status.HTTP_404_NOT_FOUND

class PermissionError(DomainError):
    code = "permission_denied"
    message = "You do not have permission."
    http_status = status.HTTP_403_FORBIDDEN

class ValidationError(DomainError):
    code = "validation_error"
    message = "Validation failed"
    http_status = status.HTTP_400_BAD_REQUEST


class DomainAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Domain error"
    default_code = "domain_error"

def raise_api_for(exc: DomainError):
    e = DomainAPIException(detail={"code": exc.code, "message": str(exc)})
    e.status_code = exc.http_status
    raise e
