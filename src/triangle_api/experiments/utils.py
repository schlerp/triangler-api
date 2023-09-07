import secrets
from datetime import datetime
from datetime import timedelta

from django.conf import settings


def generate_unique_token() -> str:
    return "".join(
        [str(secrets.randbelow(10)) for _ in range(settings.OBSERVATION_TOKEN_LENGTH)]
    )


def calculate_expiry_date() -> datetime:
    return datetime.now() + timedelta(days=1)
