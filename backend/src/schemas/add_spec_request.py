from openapi_spec_validator import validate
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError
from pydantic import BaseModel
from pydantic import field_validator


class AddSpecRequest(BaseModel):
    spec: dict

    @field_validator("spec")
    def validate_spec(cls, value):
        try:

            validate(value)
        except OpenAPIValidationError as e:
            raise ValueError(f"Invalid OpenAPI format: {e.message}")
        return value
