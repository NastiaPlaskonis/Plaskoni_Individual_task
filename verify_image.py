"""
Verification summary:
---------------------
- Input:
    • image_with_signature.png : PNG file with an embedded digital signature
    • public_key.pem : RSA public key for signature validation

- Output:
    • Console message confirming whether the signature is valid or not

Method:
This script extracts a base64-encoded RSA (4096-bit) signature from the image metadata,
recomputes the SHA-256 hash of the image content, and verifies the signature using the public key.
"""

import base64
import io

from PIL import Image
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def extract_metadata_signature(file_path: str) -> tuple[str, Image.Image]:
    """
    Opens a PNG image and retrieves the base64 signature from its metadata.

    Args:
        file_path: Path to the signed image.

    Returns:
        A tuple with the base64-encoded signature and the image object.
    """
    with Image.open(file_path) as img:
        signature = img.text.get("Signature")
        return signature, img.copy()


def deserialize_public_key(pem_path: str):
    """
    Loads and parses an RSA public key from a PEM-formatted file.

    Args:
        pem_path: Path to the PEM file.

    Returns:
        A public key object usable for signature verification.
    """
    with open(pem_path, "rb") as pem_file:
        return serialization.load_pem_public_key(pem_file.read())


def image_to_bytes(image: Image.Image) -> bytes:
    """
    Converts a Pillow Image object into raw PNG byte data, excluding metadata.

    Args:
        image: The Pillow Image object.

    Returns:
        Byte stream of the image content.
    """
    stream = io.BytesIO()
    image.save(stream, format="PNG")
    return stream.getvalue()


def validate_signature(content: bytes, signature: bytes, pub_key) -> bool:
    """
    Validates the RSA signature against the image data hash.

    Args:
        content: Byte stream of the image.
        signature: RSA signature in bytes.
        pub_key: The public key used for verification.

    Returns:
        True if signature is valid, False otherwise.
    """
    hash_func = hashes.Hash(hashes.SHA256())
    hash_func.update(content)
    digest = hash_func.finalize()

    try:
        pub_key.verify(
            signature,
            digest,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


def run_verification() -> None:
    """
    Entry point of the script that performs signature verification.
    """
    image_path = "image_with_signature.png"
    key_path = "public_key.pem"

    signature_str, img_obj = extract_metadata_signature(image_path)

    if not signature_str:
        print("No signature found in the image metadata.")
        return

    decoded_signature = base64.b64decode(signature_str)
    raw_image_bytes = image_to_bytes(img_obj)
    public_key = deserialize_public_key(key_path)

    if validate_signature(raw_image_bytes, decoded_signature, public_key):
        print("The signature is valid and the image is authentic.")
    else:
        print("The signature is invalid or the image has been tampered with.")


if __name__ == "__main__":
    run_verification()