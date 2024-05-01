::: scooze.utils
    options:
        filters:
            - "!to_lower_camel"
            - "!JsonNormalizer"
            - "!ScoozeRotatingFileHandler"
            - "!JsonLoggingFormatter"

::: scooze.enums
    options:
        inherited_members: false
