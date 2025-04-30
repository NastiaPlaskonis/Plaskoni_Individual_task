# Image signature with RSA and SHA-256

> Developed by **Anastasiia Plaskonis**  
> as part of the Information Security Fundamentals course  
> Ukrainian Catholic University, 2025

This repository contains a compact solution for securely signing PNG images using RSA (4096-bit) and SHA-256 hashing. The signature is written directly into the image's metadata — invisible to the viewer but verifiable by cryptographic means.

---

## Purpose

In an era of AI-generated content and misinformation, verifying the source and integrity of digital images is essential.

This project allows you to:
- confirm that an image is issued by a trusted source
- detect any post-signature alterations — even a single pixel
- embed cryptographic authenticity into standard image files

**Real-world applications:**
- Verified publication of digital documents or media  
- Secure communication in forensic, journalistic, or legal contexts  
- Educational demonstration of public key cryptography applied to real-world content

---

## Overview of the process

### Signing

The `sign_image.py` script:
- reads a PNG image
- computes its SHA-256 hash from pixel data
- signs the hash using a private RSA key
- stores the Base64-encoded signature in the PNG metadata

### Verification

The `verify_image.py` script:
- loads the signed image
- retrieves the embedded signature
- re-hashes the image content
- validates the signature using the public RSA key

> Any mismatch will flag the image as modified or untrusted.

---

## Key generation (external)

Use OpenSSL to generate RSA keys:

```bash
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:4096
openssl rsa -pubout -in private_key.pem -out public_key.pem
```

## Getting started

### Requirements

- **Python 3.8+**

- Dependencies:
  - `Pillow`
  - `cryptography`

Install all dependencies using:

```bash
pip install -r requirements.txt
```

### How to use

1. **Prepare your image**
   - Save the image as `image.png` in the project folder.

2. **Run the signing script**

```bash
python3 sign_image.py
```
This will generate a new file called `image_with_signature.png` containing the embedded signature.

3. **Run the verification script**

```bash
python3 verify_image.py
```
## Project structure

```text
├── image.png                   >> Source image to be signed
├── image_with_signature.png    >> Resulting image with embedded signature
├── private_key.pem             >> RSA private key (keep secure)
├── public_key.pem              >> RSA public key (safe to share)
├── sign_image.py               >> Script for signing the image
├── verify_image.py             >> Script for verifying the image
├── requirements.txt            >> Python dependencies
└── README.md                   >> Project documentation
```

## Technical highlights

- Uses only the image’s visual content for hashing (metadata is ignored)
- Signature is stored using native PNG metadata (invisible to viewer)
- Opens in any image viewer — no compatibility issues
- Clean, modular code following [PEP 8](https://peps.python.org/pep-0008/) and `pylint` standards

---

### Optional extensions

- Hide signature in pixels via steganography
- Add timestamps or blockchain anchoring
- Support for multiple signatures or embedded watermarks

---

## Final outcome

By combining cryptographic precision with seamless image compatibility,  
this solution ensures that digital visuals can carry invisible proof of origin.  
Every signed file maintains its original look — but gains verifiable trust.
