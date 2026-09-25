"""

Utilidad para generar un secret_key seguro en JWT

"""

import argparse
import secrets

def generate_secret_key(num_bytes: int = 32) -> str:
    # Genera una cadena hexadecimal criptográficamente segura.
    # num_bytes: produce una cadena de 64 caracteres hexadecimal suficiente para HS256

    return secrets.token_hex(num_bytes)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera un SECRET_KEY para JWT")
    parser.add_argument(
        "--bytes",
        type=int,
        default=32,
        help="Cantidad de bytes aleatorios (default: 32 → 64 caracteres hex)",
    )
    args = parser.parse_args()

    key = generate_secret_key(args.bytes)
    print(f"\nSECRET_KEY={key}\n")
