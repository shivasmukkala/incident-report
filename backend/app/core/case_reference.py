import secrets


def generate_case_reference() -> str:
    """Generate a unique-looking public-facing case reference."""
    random_part = secrets.token_hex(8).upper()
    return f"IR-{random_part}"
