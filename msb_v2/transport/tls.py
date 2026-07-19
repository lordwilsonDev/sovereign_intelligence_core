from __future__ import annotations

import datetime
import os
from pathlib import Path
from typing import Optional

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID


def _ensure_dir(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def write_self_signed_cert(cert_path: str, key_path: str, common_name: str = "localhost", days: int = 365) -> dict:
    _ensure_dir(cert_path)
    _ensure_dir(key_path)
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "MSB v2 Test"),
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc).replace(minute=0, second=0, microsecond=0))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=days))
        .add_extension(x509.SubjectAlternativeName([x509.DNSName(common_name)]), critical=False)
        .sign(key, hashes.SHA256())
    )
    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    Path(cert_path).write_bytes(cert_pem)
    Path(key_path).write_bytes(key_pem)
    return {"cert_path": cert_path, "key_path": key_path, "common_name": common_name, "days": days}


def resolve_tls_paths(cert_path: Optional[str], key_path: Optional[str]) -> Optional[tuple[str, str]]:
    if not cert_path or not key_path:
        return None
    c = Path(cert_path).expanduser().resolve()
    k = Path(key_path).expanduser().resolve()
    if c.exists() and k.exists():
        return str(c), str(k)
    base_name = c.stem if c.stem else "msb-self-signed"
    default_cert = str(c.with_name(f"{base_name}.crt").resolve())
    default_key = str(c.with_name(f"{base_name}.key").resolve())
    if Path(default_cert).exists() and Path(default_key).exists():
        return default_cert, default_key
    return None


def start(app: object, host: str, port: int, cert_path: Optional[str], key_path: Optional[str], reload: bool = False) -> str:
    import uvicorn
    tls_pair = resolve_tls_paths(cert_path, key_path)
    if tls_pair:
        c, k = tls_pair
        uvicorn.run(app, host=host, port=int(port), ssl_certfile=c, ssl_keyfile=k)
        return f"tls://{host}:{port}"
    uvicorn.run(app, host=host, port=int(port), reload=reload)
    return f"http://{host}:{port}"
