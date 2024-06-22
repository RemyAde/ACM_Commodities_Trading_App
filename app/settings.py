from dotenv import dotenv_values

configuration_credentials = dotenv_values(".env")

DATABASE_URL = configuration_credentials["DATABASE_URL"]


TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL
    },
    "apps": {
        "models": {
            "models": [
                "aerich.models",
                "app.db.models.user",
                "app.db.models.admin",
            ],
            "default_connection": "default"
        },
    },
}