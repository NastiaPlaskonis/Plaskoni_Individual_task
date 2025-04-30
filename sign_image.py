"""
Usage summary:
--------------
- Input:
    • image.png : image to sign
    • private_key.pem : RSA key used for signing

- Output:
    • image_with_signature.png : image with embedded digital signature

Method:
This script uses SHA-256 hashing and RSA (4096-bit) for secure signing.
Signature is stored in the PNG metadata.
"""

import base64
import io

from PIL import Image, PngImagePlugin
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def read_private_key(path: str):
    """
    Reads and deserializes the RSA private key from a PEM file.
    """
    with open(path, "rb") as file:
        return serialization.load_pem_private_key(
            file.read(),
            password=None,
        )


def extract_image_bytes(image_path: str) -> tuple[bytes, Image.Image]:
    """
    Opens the image and returns its byte stream and Pillow object.
    """
    with Image.open(image_path) as img:
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue(), img.copy()


def generate_signature(payload: bytes, key) -> str:
    """
    Generates a base64-encoded RSA digital signature for the input bytes.
    """
    hasher = hashes.Hash(hashes.SHA256())
    hasher.update(payload)
    digest = hasher.finalize()

    raw_signature = key.sign(
        digest,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return base64.b64encode(raw_signature).decode("utf-8")


def attach_signature(image: Image.Image, signature: str, destination: str) -> None:
    """
    Attaches the signature string to image metadata and writes to disk.
    """
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("Signature", signature)
    image.save(destination, format="PNG", pnginfo=metadata)


def run_signing_pipeline() -> None:
    """
    Coordinates the signing workflow: load image, sign, embed, save.
    """
    img_path = "image.png"
    key_path = "private_key.pem"
    output_path = "image_with_signature.png"

    data, image_obj = extract_image_bytes(img_path)
    private_key = read_private_key(key_path)
    b64_signature = generate_signature(data, private_key)
    attach_signature(image_obj, b64_signature, output_path)

    print("The image successfully signed and saved as 'image_with_signature.png'")


if __name__ == "__main__":
    run_signing_pipeline()