from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_keys():
    # Generate a private RSA key with a standard public exponent (65537) and 2048-bit size
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Serialize the private key into PEM format, unencrypted PKCS8
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Extract the public key from the private key and serialize it to PEM format
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Save the keys to files with clear names
    with open("private_key.pem", "wb") as f:
        f.write(private_pem)
    
    with open("public_key.pem", "wb") as f:
        f.write(public_pem)

    # Output status to terminal
    print("RSA 2048-bit key pair created")
    print("Key files generated")

if __name__ == "__main__":
    generate_keys() # Execute key generation when script is run
