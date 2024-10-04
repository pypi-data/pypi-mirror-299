from django.conf import settings
from django.core.checks import Error
from django.core.checks import Warning as CheckWarning
from django.core.checks import register
from django.db import OperationalError, connection


@register()
def check_postgres_extensions(app_configs, **_kwargs):
    errors = []
    warnings = []

    # Dynamically check the database engine
    database_engine = settings.DATABASES["default"]["ENGINE"]
    if "postgresql" in database_engine:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM pg_extension WHERE extname='pg_trgm';")
                result = cursor.fetchone()
                if not result:
                    errors.append(
                        Error(
                            "pg_trgm extension is not installed",
                            hint=(
                                "Run `CREATE EXTENSION pg_trgm;` in "
                                "your PSQL database."
                            ),
                            id="postgres.E001",
                        )
                    )
        except OperationalError as error:
            errors.append(
                Error(
                    f"Error checking pg_trgm extension: {error}",
                    hint="Ensure your database is running and accessible.",
                    id="postgres.E002",
                )
            )
    else:
        warnings.append(
            CheckWarning(
                "Database engine is not PostgreSQL.",
                hint=(
                    "PostgreSQL improves search in `django-sage-blog`, "
                    "but it's optional."
                ),
                id="postgres.W001",
            )
        )

    return errors + warnings
