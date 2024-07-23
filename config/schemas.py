import re

from pydantic import BaseModel, EmailStr, field_validator

from config.validators_exception import ValidationError


class SignUp(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    def email_validator(
            cls,
            value: str
    ) -> str | ValueError:
        """
        Check Input Email
        """
        if not value.endswith("@gmail.com") and not value.endswith("@ukr.net"):
            raise ValidationError(f"Expected: @gmail.com or @ukr.net but got {value}")
        else:
            return value

    @field_validator("password")
    def password_validator(
            cls,
            value: str
    ) -> str | ValueError:
        """
        Check Input Password
        """
        if len(value) < 8 or len(value) > 16:
            raise ValidationError("Password must contain between 8 and 16 characters long")
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', value):
            raise ValidationError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_]', value):
            raise ValidationError("Password must contain at least one special character")
        return value
