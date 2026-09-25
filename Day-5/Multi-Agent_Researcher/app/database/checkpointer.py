from app.config.settings import settings


def get_database_url() -> str:
    if not settings.DATABASE_URL:
        raise ValueError(
            "DATABASE_URL is not configured in the .env file."
        )

    return settings.DATABASE_URL