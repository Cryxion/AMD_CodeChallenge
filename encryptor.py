import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def encrypt_file(input_file, public_key_file, output_file):
    # Load the RSA Public Key from a PEM file
    with open(public_key_file, "rb") as kf:
        public_key = serialization.load_pem_public_key(kf.read())

    # Generate a random 256-bit AES key and a 12-byte IV for GCM mode
    aes_key = os.urandom(32)
    iv = os.urandom(12)

    # Encrypt the temporary AES key using the RSA Public Key and OAEP padding
    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Read the entire original file data
    with open(input_file, "rb") as f:
        data = f.read()

    # Initialize the AES-GCM cipher for encryption
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    # Encrypt the data and generate an authentication tag
    ciphertext = encryptor.update(data) + encryptor.finalize()
    tag = encryptor.tag

    # Store the metadata and ciphertext: [AES Key Length][Encrypted AES Key][IV][Tag][Ciphertext]
    with open(output_file, "wb") as f:
        f.write(len(encrypted_aes_key).to_bytes(4, byteorder='big')) # Write length of RSA block
        f.write(encrypted_aes_key) # Write the RSA-wrapped AES key
        f.write(iv) # Write the 12-byte IV
        f.write(tag) # Write the 16-byte GCM tag
        f.write(ciphertext) # Write the encrypted file content

def decrypt_file(input_file, private_key_file, output_file):
    # Load the RSA Private Key from a PEM file
    with open(private_key_file, "rb") as kf:
        private_key = serialization.load_pem_private_key(kf.read(), password=None)

    # Parse the encrypted file format [AES Key Length][Encrypted AES Key][IV][Tag][Ciphertext]
    with open(input_file, "rb") as f:
        key_len = int.from_bytes(f.read(4), byteorder='big') # Get length of RSA block
        encrypted_aes_key = f.read(key_len) # Read the RSA-wrapped AES key
        iv = f.read(12) # Read the 12-byte IV
        tag = f.read(16) # Read the 16-byte GCM tag
        ciphertext = f.read() # Read the remainder

    # Decrypt the AES key using the RSA Private Key and OAEP padding
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Initialize the AES-GCM cipher for decryption using the recovered key and tag
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv, tag))
    decryptor = cipher.decryptor()
    # Decrypt and verify the integrity of the data
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Save the recovered original file data
    with open(output_file, "wb") as f:
        f.write(decrypted_data)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python encryptor.py encrypt/decrypt <filename>")
    else:
        mode = sys.argv[1]
        filename = sys.argv[2]
        if mode == "encrypt":
            encrypt_file(filename, "public_key.pem", "encrypted_file.bin")
            print("Done: File is now locked in encrypted_file.bin")
        elif mode == "decrypt":
            decrypt_file(filename, "private_key.pem", "recovered_file.jpg")
            print("Done: File extracted to recovered_file.jpg")
