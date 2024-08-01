import re

from pydantic import BaseModel, EmailStr, field_validator

from config.validators_exception import ValidationError


class SignUpOrLogin(BaseModel):
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


class PostAdd(BaseModel):
    text: str

    @field_validator("text")
    def text_validator(
            cls,
            value: str
    ) -> str | ValueError:
        """
        Check Input Text
        """
        # If Payload Large than 1 MB
        if len(value.encode('utf-8')) > 1 * 1024 * 1024:
            raise ValidationError('Payload Too Large')

        # Only allow letters, numbers, spaces, and common punctuation
        if not re.match("^[a-zA-Z0-9\s.,!?]*$", value):
            raise ValidationError("Text Contains Invalid Characters")

        # Minimum 5 Words
        if len(value.split()) < 5:
            raise ValidationError("Text must contain at least 5 words")

        return value


class PostDelete(BaseModel):
    post_id: int

    @field_validator("post_id", mode="before")
    def post_id_validator(
            cls,
            value: str
    ) -> int | ValidationError:
        """
        Check Input Post Id
        """

        if not isinstance(value, int):
            raise ValidationError("Post Id Can be Only Integer")

        return value
